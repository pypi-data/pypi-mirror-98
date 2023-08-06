import { __extends, __makeTemplateObject } from "tslib";
import 'react-date-range/dist/styles.css';
import 'react-date-range/dist/theme/default.css';
import React from 'react';
import { DateRangePicker } from 'react-date-range';
import styled from '@emotion/styled';
import moment from 'moment';
import PropTypes from 'prop-types';
import Checkbox from 'app/components/checkbox';
import TimePicker from 'app/components/organizations/timeRangeSelector/timePicker';
import { MAX_PICKABLE_DAYS } from 'app/constants';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { analytics } from 'app/utils/analytics';
import { getEndOfDay, getStartOfPeriodAgo, isValidTime, setDateToTime, } from 'app/utils/dates';
import getRouteStringFromRoutes from 'app/utils/getRouteStringFromRoutes';
import theme from 'app/utils/theme';
var getTimeStringFromDate = function (date) { return moment(date).local().format('HH:mm'); };
function isRangeSelection(maybe) {
    return maybe.selection !== undefined;
}
var defaultProps = {
    showAbsolute: true,
    showRelative: false,
    /**
     * The maximum number of days in the past you can pick
     */
    maxPickableDays: MAX_PICKABLE_DAYS,
};
var DateRange = /** @class */ (function (_super) {
    __extends(DateRange, _super);
    function DateRange() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            hasStartErrors: false,
            hasEndErrors: false,
        };
        _this.handleSelectDateRange = function (changeProps) {
            if (!isRangeSelection(changeProps)) {
                return;
            }
            var selection = changeProps.selection;
            var onChange = _this.props.onChange;
            var startDate = selection.startDate, endDate = selection.endDate;
            var end = endDate ? getEndOfDay(endDate) : endDate;
            onChange({
                start: startDate,
                end: end,
            });
        };
        _this.handleChangeStart = function (e) {
            var _a, _b;
            // Safari does not support "time" inputs, so we don't have access to
            // `e.target.valueAsDate`, must parse as string
            //
            // Time will be in 24hr e.g. "21:00"
            var start = (_a = _this.props.start) !== null && _a !== void 0 ? _a : '';
            var end = (_b = _this.props.end) !== null && _b !== void 0 ? _b : undefined;
            var onChange = _this.props.onChange;
            var startTime = e.target.value;
            if (!startTime || !isValidTime(startTime)) {
                _this.setState({ hasStartErrors: true });
                onChange({ hasDateRangeErrors: true });
                return;
            }
            var newTime = setDateToTime(start, startTime, { local: true });
            analytics('dateselector.time_changed', {
                field_changed: 'start',
                time: startTime,
                path: getRouteStringFromRoutes(_this.context.router.routes),
                org_id: parseInt(_this.props.organization.id, 10),
            });
            onChange({
                start: newTime,
                end: end,
                hasDateRangeErrors: _this.state.hasEndErrors,
            });
            _this.setState({ hasStartErrors: false });
        };
        _this.handleChangeEnd = function (e) {
            var _a, _b;
            var start = (_a = _this.props.start) !== null && _a !== void 0 ? _a : undefined;
            var end = (_b = _this.props.end) !== null && _b !== void 0 ? _b : '';
            var onChange = _this.props.onChange;
            var endTime = e.target.value;
            if (!endTime || !isValidTime(endTime)) {
                _this.setState({ hasEndErrors: true });
                onChange({ hasDateRangeErrors: true });
                return;
            }
            var newTime = setDateToTime(end, endTime, { local: true });
            analytics('dateselector.time_changed', {
                field_changed: 'end',
                time: endTime,
                path: getRouteStringFromRoutes(_this.context.router.routes),
                org_id: parseInt(_this.props.organization.id, 10),
            });
            onChange({
                start: start,
                end: newTime,
                hasDateRangeErrors: _this.state.hasStartErrors,
            });
            _this.setState({ hasEndErrors: false });
        };
        return _this;
    }
    DateRange.prototype.render = function () {
        var _a, _b;
        var _c = this.props, className = _c.className, maxPickableDays = _c.maxPickableDays, utc = _c.utc, showTimePicker = _c.showTimePicker, onChangeUtc = _c.onChangeUtc;
        var start = (_a = this.props.start) !== null && _a !== void 0 ? _a : '';
        var end = (_b = this.props.end) !== null && _b !== void 0 ? _b : '';
        var startTime = getTimeStringFromDate(new Date(start));
        var endTime = getTimeStringFromDate(new Date(end));
        // Restraints on the time range that you can select
        // Can't select dates in the future b/c we're not fortune tellers (yet)
        //
        // We want `maxPickableDays` - 1 (if today is Jan 5, max is 3 days, the minDate should be Jan 3)
        // Subtract additional day  because we force the end date to be inclusive,
        // so when you pick Jan 1 the time becomes Jan 1 @ 23:59:59,
        // (or really, Jan 2 @ 00:00:00 - 1 second), while the start time is at 00:00
        var minDate = getStartOfPeriodAgo('days', maxPickableDays - 2);
        var maxDate = new Date();
        return (<div className={className} data-test-id="date-range">
        <StyledDateRangePicker rangeColors={[theme.purple300]} ranges={[
            {
                startDate: moment(start).local().toDate(),
                endDate: moment(end).local().toDate(),
                key: 'selection',
            },
        ]} minDate={minDate} maxDate={maxDate} onChange={this.handleSelectDateRange}/>
        {showTimePicker && (<TimeAndUtcPicker>
            <TimePicker start={startTime} end={endTime} onChangeStart={this.handleChangeStart} onChangeEnd={this.handleChangeEnd}/>
            <UtcPicker>
              {t('Use UTC')}
              <Checkbox onChange={onChangeUtc} checked={utc || false} style={{
            margin: '0 0 0 0.5em',
        }}/>
            </UtcPicker>
          </TimeAndUtcPicker>)}
      </div>);
    };
    DateRange.contextTypes = {
        router: PropTypes.object,
    };
    DateRange.defaultProps = defaultProps;
    return DateRange;
}(React.Component));
var StyledDateRange = styled(DateRange)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  border-left: 1px solid ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  border-left: 1px solid ", ";\n"])), function (p) { return p.theme.border; });
var StyledDateRangePicker = styled(DateRangePicker)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: 21px; /* this is specifically so we can align borders */\n\n  .rdrSelected,\n  .rdrInRange,\n  .rdrStartEdge,\n  .rdrEndEdge {\n    background-color: ", ";\n  }\n\n  .rdrStartEdge + .rdrDayStartPreview {\n    background-color: transparent;\n  }\n\n  .rdrDayNumber span {\n    color: ", ";\n  }\n\n  .rdrDayDisabled span {\n    color: ", ";\n  }\n\n  .rdrDayToday .rdrDayNumber span {\n    color: ", ";\n  }\n\n  .rdrDayNumber span:after {\n    background-color: ", ";\n  }\n\n  .rdrDefinedRangesWrapper,\n  .rdrDateDisplayWrapper,\n  .rdrWeekDays {\n    display: none;\n  }\n\n  .rdrInRange {\n    background: ", ";\n  }\n\n  .rdrDayInPreview {\n    background: ", ";\n  }\n\n  .rdrMonth {\n    width: 300px;\n    font-size: 1.2em;\n    padding: 0;\n  }\n\n  .rdrStartEdge {\n    border-top-left-radius: 1.14em;\n    border-bottom-left-radius: 1.14em;\n  }\n\n  .rdrEndEdge {\n    border-top-right-radius: 1.14em;\n    border-bottom-right-radius: 1.14em;\n  }\n\n  .rdrDayStartPreview,\n  .rdrDayEndPreview,\n  .rdrDayInPreview {\n    border: 0;\n    background: rgba(200, 200, 200, 0.3);\n  }\n\n  .rdrDayStartOfMonth,\n  .rdrDayStartOfWeek {\n    .rdrInRange {\n      border-top-left-radius: 0;\n      border-bottom-left-radius: 0;\n    }\n  }\n\n  .rdrDayEndOfMonth,\n  .rdrDayEndOfWeek {\n    .rdrInRange {\n      border-top-right-radius: 0;\n      border-bottom-right-radius: 0;\n    }\n  }\n\n  .rdrStartEdge.rdrEndEdge {\n    border-radius: 1.14em;\n  }\n\n  .rdrMonthAndYearWrapper {\n    padding-bottom: ", ";\n    padding-top: 0;\n    height: 32px;\n  }\n\n  .rdrDay {\n    height: 2.5em;\n  }\n\n  .rdrMonthPicker select,\n  .rdrYearPicker select {\n    background: none;\n    font-weight: normal;\n    font-size: 16px;\n    padding: 0;\n  }\n\n  .rdrMonthsVertical {\n    align-items: center;\n  }\n\n  .rdrCalendarWrapper {\n    flex: 1;\n  }\n\n  .rdrNextPrevButton {\n    background-color: transparent;\n    border: 1px solid ", ";\n  }\n\n  .rdrPprevButton i {\n    border-right-color: ", ";\n  }\n\n  .rdrNextButton i {\n    border-left-color: ", ";\n  }\n"], ["\n  padding: 21px; /* this is specifically so we can align borders */\n\n  .rdrSelected,\n  .rdrInRange,\n  .rdrStartEdge,\n  .rdrEndEdge {\n    background-color: ", ";\n  }\n\n  .rdrStartEdge + .rdrDayStartPreview {\n    background-color: transparent;\n  }\n\n  .rdrDayNumber span {\n    color: ", ";\n  }\n\n  .rdrDayDisabled span {\n    color: ", ";\n  }\n\n  .rdrDayToday .rdrDayNumber span {\n    color: ", ";\n  }\n\n  .rdrDayNumber span:after {\n    background-color: ", ";\n  }\n\n  .rdrDefinedRangesWrapper,\n  .rdrDateDisplayWrapper,\n  .rdrWeekDays {\n    display: none;\n  }\n\n  .rdrInRange {\n    background: ", ";\n  }\n\n  .rdrDayInPreview {\n    background: ", ";\n  }\n\n  .rdrMonth {\n    width: 300px;\n    font-size: 1.2em;\n    padding: 0;\n  }\n\n  .rdrStartEdge {\n    border-top-left-radius: 1.14em;\n    border-bottom-left-radius: 1.14em;\n  }\n\n  .rdrEndEdge {\n    border-top-right-radius: 1.14em;\n    border-bottom-right-radius: 1.14em;\n  }\n\n  .rdrDayStartPreview,\n  .rdrDayEndPreview,\n  .rdrDayInPreview {\n    border: 0;\n    background: rgba(200, 200, 200, 0.3);\n  }\n\n  .rdrDayStartOfMonth,\n  .rdrDayStartOfWeek {\n    .rdrInRange {\n      border-top-left-radius: 0;\n      border-bottom-left-radius: 0;\n    }\n  }\n\n  .rdrDayEndOfMonth,\n  .rdrDayEndOfWeek {\n    .rdrInRange {\n      border-top-right-radius: 0;\n      border-bottom-right-radius: 0;\n    }\n  }\n\n  .rdrStartEdge.rdrEndEdge {\n    border-radius: 1.14em;\n  }\n\n  .rdrMonthAndYearWrapper {\n    padding-bottom: ", ";\n    padding-top: 0;\n    height: 32px;\n  }\n\n  .rdrDay {\n    height: 2.5em;\n  }\n\n  .rdrMonthPicker select,\n  .rdrYearPicker select {\n    background: none;\n    font-weight: normal;\n    font-size: 16px;\n    padding: 0;\n  }\n\n  .rdrMonthsVertical {\n    align-items: center;\n  }\n\n  .rdrCalendarWrapper {\n    flex: 1;\n  }\n\n  .rdrNextPrevButton {\n    background-color: transparent;\n    border: 1px solid ", ";\n  }\n\n  .rdrPprevButton i {\n    border-right-color: ", ";\n  }\n\n  .rdrNextButton i {\n    border-left-color: ", ";\n  }\n"])), function (p) { return p.theme.active; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.active; }, function (p) { return p.theme.active; }, function (p) { return p.theme.active; }, function (p) { return p.theme.focus; }, space(1), function (p) { return p.theme.border; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
var TimeAndUtcPicker = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n  border-top: 1px solid ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n  border-top: 1px solid ", ";\n"])), space(2), function (p) { return p.theme.innerBorder; });
var UtcPicker = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n  flex: 1;\n"], ["\n  color: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n  flex: 1;\n"])), function (p) { return p.theme.gray300; });
export default StyledDateRange;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map