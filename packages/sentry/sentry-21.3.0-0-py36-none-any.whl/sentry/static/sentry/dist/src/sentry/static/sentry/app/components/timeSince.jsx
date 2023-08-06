import { __extends, __rest } from "tslib";
import React from 'react';
import isNumber from 'lodash/isNumber';
import isString from 'lodash/isString';
import moment from 'moment-timezone';
import { t } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import { getDuration } from 'app/utils/formatters';
import getDynamicText from 'app/utils/getDynamicText';
import Tooltip from './tooltip';
var ONE_MINUTE_IN_MS = 60000;
var TimeSince = /** @class */ (function (_super) {
    __extends(TimeSince, _super);
    function TimeSince() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            relative: '',
        };
        _this.ticker = null;
        _this.setRelativeDateTicker = function () {
            _this.ticker = window.setTimeout(function () {
                _this.setState({
                    relative: getRelativeDate(_this.props.date, _this.props.suffix, _this.props.shorten, _this.props.extraShort),
                });
                _this.setRelativeDateTicker();
            }, ONE_MINUTE_IN_MS);
        };
        return _this;
    }
    // TODO(ts) TODO(emotion): defining the props type breaks emotion's typings
    // See: https://github.com/emotion-js/emotion/pull/1514
    TimeSince.getDerivedStateFromProps = function (props) {
        return {
            relative: getRelativeDate(props.date, props.suffix, props.shorten, props.extraShort),
        };
    };
    TimeSince.prototype.componentDidMount = function () {
        this.setRelativeDateTicker();
    };
    TimeSince.prototype.componentWillUnmount = function () {
        if (this.ticker) {
            window.clearTimeout(this.ticker);
            this.ticker = null;
        }
    };
    TimeSince.prototype.render = function () {
        var _a;
        var _b = this.props, date = _b.date, _suffix = _b.suffix, disabledAbsoluteTooltip = _b.disabledAbsoluteTooltip, className = _b.className, tooltipTitle = _b.tooltipTitle, _shorten = _b.shorten, _extraShort = _b.extraShort, props = __rest(_b, ["date", "suffix", "disabledAbsoluteTooltip", "className", "tooltipTitle", "shorten", "extraShort"]);
        var dateObj = getDateObj(date);
        var user = ConfigStore.get('user');
        var options = user ? user.options : null;
        var format = (options === null || options === void 0 ? void 0 : options.clock24Hours) ? 'MMMM D, YYYY HH:mm z' : 'LLL z';
        var tooltip = getDynamicText({
            fixed: (options === null || options === void 0 ? void 0 : options.clock24Hours) ? 'November 3, 2020 08:57 UTC'
                : 'November 3, 2020 8:58 AM UTC',
            value: moment.tz(dateObj, (_a = options === null || options === void 0 ? void 0 : options.timezone) !== null && _a !== void 0 ? _a : '').format(format),
        });
        return (<Tooltip disabled={disabledAbsoluteTooltip} title={<div>
            <div>{tooltipTitle}</div>
            {tooltip}
          </div>}>
        <time dateTime={dateObj.toISOString()} className={className} {...props}>
          {this.state.relative}
        </time>
      </Tooltip>);
    };
    TimeSince.defaultProps = {
        suffix: 'ago',
    };
    return TimeSince;
}(React.PureComponent));
export default TimeSince;
function getDateObj(date) {
    if (isString(date) || isNumber(date)) {
        date = new Date(date);
    }
    return date;
}
export function getRelativeDate(currentDateTime, suffix, shorten, extraShort) {
    var date = getDateObj(currentDateTime);
    if ((shorten || extraShort) && suffix) {
        return t('%(time)s %(suffix)s', {
            time: getDuration(moment().diff(moment(date), 'seconds'), 0, shorten, extraShort),
            suffix: suffix,
        });
    }
    else if ((shorten || extraShort) && !suffix) {
        return getDuration(moment().diff(moment(date), 'seconds'), 0, shorten, extraShort);
    }
    else if (!suffix) {
        return moment(date).fromNow(true);
    }
    else if (suffix === 'ago') {
        return moment(date).fromNow();
    }
    else if (suffix === 'old') {
        return t('%(time)s old', { time: moment(date).fromNow(true) });
    }
    else {
        throw new Error('Unsupported time format suffix');
    }
}
//# sourceMappingURL=timeSince.jsx.map