
import json
import os
import datetime
import traceback
from typing import Dict, List, Optional

import pandas as pd
import numpy as np

from .....constant import SourceType
from .....fund.engine.trader import BasicFundTrader
from .....fund.engine.backtest import BasicFundBacktestEngine
from ....fund.basic.basic_data_helper import BasicDataHelper
from ....manager.manager_fund import FundDataManager
from ....view.derived_models import ThirdPartyPortfolioInfo, ThirdPartyPortfolioTrade, ThirdPartyPortfolioIndicator, ThirdPartyPortfolioPositionLatest
from ..derived_data_helper import DerivedDataHelper, DateJSONEncoder
from .common import ThirdPortfolioBase


class DanjuanPortfolioProcessor(ThirdPortfolioBase):

    _FILE_SUFFIX = 'json'
    _INFO_COLUMNS_MAP = {
        'portfolio_id': 'po_id',
        'plan_name': 'po_name',
        'found_date': 'start_date',
        'auto_invest_status': 'can_aip',
    }

    def __init__(self, data_helper: DerivedDataHelper):
        super().__init__()

        self._data_helper = DerivedDataHelper()
        self._params_json: Dict[str, str] = {}
        self._dir_path = f'{os.path.dirname(os.path.abspath(__file__))}/data/danjuan'
        self._trades_df_list = []
        self._nav: Dict[str, pd.DataFrame] = {}
        self._last_position: List[pd.Series] = []

    def init(self):
        # self._fdm = FundDataManager(s3_retriever_activation=True)
        # self._fdm.init(score_pre_calc=True, print_time=True)

        from .....resource.data_store import DataStore
        self._fdm: FundDataManager = DataStore.load_dm()
        self._bdh = BasicDataHelper()
        self._trading_day: pd.DataFrame = FundDataManager.basic_data('get_trading_day_list').drop(columns='_update_time')

        self._list_no_aip = pd.read_csv(f'{self._dir_path}/list_no_aip.txt', header=None, names=['file_name'])
        # self._list_no_aip = self._list_no_aip[self._list_no_aip.file_name.str.split('.', n=1, expand=True)[0].isin(['CSI1003', 'CSI1030', 'CSI1039', 'CSI1046', 'CSI1075', 'CSI1080'])]

    def _calc_basic_info(self, x: pd.Series):
        with open(f'{self._dir_path}/portfolios/{x.file_name}', 'r') as f:
            portfolio_base_info = json.load(f)

        base_info = portfolio_base_info.get('data')
        if base_info is None:
            print(f'[WARNING] Can not find info of {x.file_name}')
            return

        result = {}
        result['po_id'] = base_info.get('plan_code')
        assert result['po_id'] == x.file_name.split('.')[0], 'portfolio id does not match'
        for one in ('plan_name', 'manager_name', 'found_date', 'auto_invest_status'):
            result[one] = base_info.get(one)
        if result['auto_invest_status'] is not None:
            result['auto_invest_status'] = (result['auto_invest_status'] != '0')

        plan_desc = base_info.get('plan_desc')
        if plan_desc is not None:
            for one in plan_desc:
                if one.get('name') == '组合概要':
                    result['rich_desc'] = one.get('plan_desc')
                    break
        op_fund = base_info.get('op_fund')
        if op_fund is not None:
            result['po_desc'] = op_fund.get('recom_desc')
            result['risk_level'] = op_fund.get('risk_tag')
            result['benchmarks'] = op_fund.get('st_code')
        return pd.Series(result)

    def _calc_trades(self, x: pd.Series):
        po_id = x.file_name.split('.')[0]

        fund_weight_list = []
        result_params = {}
        result_params['fund_weight_list'] = []
        with open(f'{self._dir_path}/portfolios/{po_id}_adj.{self._FILE_SUFFIX}', 'r') as f:
            adj_info = json.load(f)

        content = adj_info.get('data')
        if content is None:
            print(f'[WARNING] Invalid content {adj_info}')
        items = content.get('items')
        if items is None:
            print(f'[WARNING] Invalid items {content}')

        for one_item in items:
            assert one_item.get('plan_code') == po_id, 'portfolio id does not match'
            trade_date = datetime.date.fromtimestamp(one_item.get('trade_date') / 1000)
            details = one_item.get('trading_elements')
            if details is None:
                print(f'[WARNING] Invalid details {one_item}')
                continue
            if not details:
                print(f'[INFO] Empty details, do next one')
                continue
            fp_sum = 0
            tp_sum = 0
            result_details = []
            for one in details:
                raw_fund_id = one.get('fd_code')
                fund_id = self._bdh._get_fund_id_from_order_book_id(raw_fund_id, trade_date)
                if fund_id is None:
                    print(f'[WARNING] Can not found fund {raw_fund_id} (po_id){po_id}')
                    fund_id = raw_fund_id + '!0'
                from_percent = one.get('last_portion')
                to_percent = one.get('portion')
                result_details.append({'fund_id': fund_id, 'from_percent': from_percent, 'to_percent': to_percent})
                fp_sum += from_percent
                tp_sum += to_percent
            fp_sum = round(fp_sum, 3)
            tp_sum = round(tp_sum, 3)
            if (fp_sum != 0 and fp_sum != 1) or tp_sum != 1:
                print(f'sum of percent not equals 1 (po_id){po_id} (trade_date){trade_date} (fp_sum){fp_sum} (tp_sum){tp_sum}')
            adjusted_date = trade_date
            # 我们是第二天调仓，因此这里调整为之前的第一个交易日
            adjusted_date = self._trading_day[self._trading_day.datetime < adjusted_date].datetime.array[-1]
            fund_weight_list.append({'po_id': po_id, 'datetime': trade_date, 'details': json.dumps(result_details), 'comment': one_item.get('remark')})
            result_params['fund_weight_list'].append([adjusted_date, [(one['fund_id'], one['to_percent']) for one in result_details]])
        self._trades_df_list.append(pd.DataFrame(fund_weight_list))

        with open(f'{self._dir_path}/portfolios/{x.file_name}', 'r') as f:
            portfolio_base_info = json.load(f)
        base_info = portfolio_base_info.get('data')
        if base_info is None:
            print(f'[WARNING] Can not find info of {x.file_name}')
        else:
            result_params['start_date'] = base_info.get('found_date')
            plan_derived = base_info.get('plan_derived')
            if plan_derived is not None:
                result_params['end_date'] = plan_derived.get('end_date')
            else:
                print(f'[WARNING] Can not find end_date of {x.file_name}')
                result_params['end_date'] = datetime.date.today().isoformat()
        result_params['fund_weight_list'].sort(key=lambda x: x[0])
        self._params_json[po_id] = json.dumps(result_params, indent=4, cls=DateJSONEncoder)

    def _calc_indicators(self, x: pd.Series):
        po_id = x.file_name.split('.')[0]
        params = json.loads(self._params_json.get(po_id))

        # print(po_id)
        # print(params)
        start_date = pd.to_datetime(params.get('start_date'), infer_datetime_format=True).date()
        # 我们是第二天调仓，因此这里调整为之前的第一个交易日
        start_date = self._trading_day[self._trading_day.datetime < start_date].datetime.array[-1]
        # end_date = pd.to_datetime(params.get('end_date'), infer_datetime_format=True).date()

        t = BasicFundTrader()
        b = BasicFundBacktestEngine(data_manager=self._fdm, trader=t, fund_weight_list=params['fund_weight_list'])
        b.init()
        b.run(start_date=start_date, end_date=None, print_time=False)

        last_position: Optional[pd.DataFrame] = b.get_last_position()
        if last_position is None:
            print(f'[WARNING] {po_id} has no last position')
        else:
            self._last_position.append(pd.Series({'po_id': po_id, 'datetime': last_position.index.name, 'po_src': SourceType.danjuan, 'position': last_position.loc[:, 'weight'].to_json()}))

        result = b.get_fund_result()
        if result is None:
            print(f'[WARNING] {po_id} has no fund result')
            return
        # 只保留我们需要的回测结果
        result = {k: v for k, v in result.items() if k in ('market_value', 'last_unit_nav', 'mdd', 'annual_ret', 'mdd_d1', 'mdd_d2', 'total_commission', 'rebalance_times')}
        result['datetime'] = result['market_value'].index.array[-1]
        result['from_setup_ret'] = result['last_unit_nav'] - 1
        resampled = result['market_value'].copy()
        resampled.index = pd.to_datetime(resampled.index)
        resampled_w = resampled.mv.resample('1W').apply(lambda x: x[-1] if not x.empty else np.nan)
        result['vol_by_week'] = resampled_w.dropna().pct_change().std(ddof=1) * np.sqrt(52)

        resampled_m = resampled.mv.resample('1M').apply(lambda x: x[-1] if not x.empty else np.nan)
        result['vol_by_month'] = resampled_m.dropna().pct_change().std(ddof=1) * np.sqrt(12)
        result['vol_by_day'] = resampled.mv.dropna().pct_change().std(ddof=1) * np.sqrt(244)
        result['annual_compounded_ret'] = np.power(result['last_unit_nav'], 1 / (result['market_value'].shape[0] / 244)) - 1
        if result['vol_by_week'] != 0:
            result['sharpe_ratio'] = (result['annual_compounded_ret'] - 0.02) / result['vol_by_week']
        else:
            result['sharpe_ratio'] = np.nan
        # 遍历每个需要计算的时间区间
        for name, value in self._DIM_TYPE.items():
            bd = (result['datetime'] - value).date()
            # 试图寻找bd及其之前的最近一天
            filtered_mv = result['market_value'].loc[result['market_value'].index <= bd, :]
            if filtered_mv.empty:
                continue
            # 计算区间内的return
            result[name] = result['market_value'].mv.array[-1] / filtered_mv.mv.array[-1] - 1

        result['nav'] = result['last_unit_nav']
        result['po_id'] = po_id
        self._nav[po_id] = result['market_value'].mv / result['market_value'].mv.array[0]
        self._nav[po_id].index = self._nav[po_id].index.map(lambda x: x.isoformat())
        # 删掉我们不需要的回测结果
        for one in ('market_value', 'last_unit_nav'):
            del result[one]
        print(f'{po_id} done')
        return pd.Series(result)

    def calc(self):
        basic_info: pd.DataFrame = self._list_no_aip.apply(self._calc_basic_info, axis=1)
        basic_info['po_src'] = SourceType.danjuan
        self._data_helper._upload_derived(basic_info.rename(columns=self._INFO_COLUMNS_MAP), ThirdPartyPortfolioInfo.__table__.name)

        self._list_no_aip.apply(self._calc_trades, axis=1)
        trades = pd.concat(self._trades_df_list)
        trades['po_src'] = SourceType.danjuan
        self._data_helper._upload_derived(trades, ThirdPartyPortfolioTrade.__table__.name)

        indicators: pd.DataFrame = self._list_no_aip.apply(self._calc_indicators, axis=1)
        indicators = indicators[indicators.notna().any(axis=1)]
        indicators['po_src'] = SourceType.danjuan
        self._data_helper._upload_derived(indicators, ThirdPartyPortfolioIndicator.__table__.name)

        last_position = pd.DataFrame(self._last_position)
        self._data_helper._upload_derived(last_position, ThirdPartyPortfolioPositionLatest.__table__.name)

        # nav存cas
        from ....view.cas.third_party_portfolio_nav import ThirdPartyPortfolioNav
        for po_id, mv in self._nav.items():
            ThirdPartyPortfolioNav.create(
                po_id=po_id,
                date=mv.index.to_list(),
                nav=mv.to_list(),
            )

    def process(self, end_date: str) -> List[str]:
        failed_tasks: List[str] = []
        try:
            self.calc_everyday(end_date, [SourceType.danjuan.value])
        except Exception as e:
            print(e)
            traceback.print_exc()
            failed_tasks.append('third_party_portfolio_danjuan')
        return failed_tasks


if __name__ == '__main__':
    danjuan_pp = DanjuanPortfolioProcessor(DerivedDataHelper())
    # danjuan_pp.init()
    # danjuan_pp.calc()
    # danjuan_pp.process('20201012')
