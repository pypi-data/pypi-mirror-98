import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { isStacktraceNewestFirst } from 'app/components/events/interfaces/stacktrace';
import StacktraceContent from 'app/components/events/interfaces/stacktraceContent';
import Hovercard, { Body } from 'app/components/hovercard';
import LoadingIndicator from 'app/components/loadingIndicator';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { EntryType } from 'app/types/event';
import { defined } from 'app/utils';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
import findBestThread from './events/interfaces/threads/threadSelector/findBestThread';
import getThreadStacktrace from './events/interfaces/threads/threadSelector/getThreadStacktrace';
export var STACKTRACE_PREVIEW_TOOLTIP_DELAY = 1000;
var StacktracePreview = /** @class */ (function (_super) {
    __extends(StacktracePreview, _super);
    function StacktracePreview() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            loadingVisible: false,
        };
        _this.loaderTimeout = null;
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, issueId, event_1, _b;
            var _this = this;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (this.state.event) {
                            return [2 /*return*/];
                        }
                        this.loaderTimeout = window.setTimeout(function () {
                            _this.setState({ loadingVisible: true });
                        }, 1000);
                        _a = this.props, api = _a.api, issueId = _a.issueId;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + issueId + "/events/latest/")];
                    case 2:
                        event_1 = _c.sent();
                        clearTimeout(this.loaderTimeout);
                        this.setState({ event: event_1, loading: false, loadingVisible: false });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        clearTimeout(this.loaderTimeout);
                        this.setState({ loading: false, loadingVisible: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleStacktracePreviewClick = function (event) {
            event.stopPropagation();
            event.preventDefault();
        };
        return _this;
    }
    StacktracePreview.prototype.getStacktrace = function () {
        var _a, _b, _c, _d, _e, _f, _g, _h;
        var event = this.state.event;
        if (!event) {
            return undefined;
        }
        var exceptionsWithStacktrace = (_c = (_b = (_a = event.entries
            .find(function (e) { return e.type === EntryType.EXCEPTION; })) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b.values.filter(function (_a) {
            var stacktrace = _a.stacktrace;
            return defined(stacktrace);
        })) !== null && _c !== void 0 ? _c : [];
        var exceptionStacktrace = isStacktraceNewestFirst()
            ? (_d = exceptionsWithStacktrace[exceptionsWithStacktrace.length - 1]) === null || _d === void 0 ? void 0 : _d.stacktrace : (_e = exceptionsWithStacktrace[0]) === null || _e === void 0 ? void 0 : _e.stacktrace;
        if (exceptionStacktrace) {
            return exceptionStacktrace;
        }
        var threads = (_h = (_g = (_f = event.entries.find(function (e) { return e.type === EntryType.THREADS; })) === null || _f === void 0 ? void 0 : _f.data) === null || _g === void 0 ? void 0 : _g.values) !== null && _h !== void 0 ? _h : [];
        var bestThread = findBestThread(threads);
        if (!bestThread) {
            return undefined;
        }
        var bestThreadStacktrace = getThreadStacktrace(false, bestThread);
        if (bestThreadStacktrace) {
            return bestThreadStacktrace;
        }
        return undefined;
    };
    StacktracePreview.prototype.renderHovercardBody = function () {
        var _a, _b;
        var _c = this.state, event = _c.event, loading = _c.loading, loadingVisible = _c.loadingVisible;
        var stacktrace = this.getStacktrace();
        if (loading && loadingVisible) {
            return (<NoStackTraceWrapper>
          <LoadingIndicator hideMessage size={48}/>
        </NoStackTraceWrapper>);
        }
        if (loading) {
            return null;
        }
        if (!stacktrace) {
            return (<NoStackTraceWrapper onClick={this.handleStacktracePreviewClick}>
          {t("There's no stack trace available for this issue.")}
        </NoStackTraceWrapper>);
        }
        if (event) {
            trackAnalyticsEvent({
                eventKey: 'stacktrace.preview.open',
                eventName: 'Stack Trace Preview: Open',
                organization_id: parseInt(this.props.organization.id, 10),
                issue_id: this.props.issueId,
            });
            return (<div onClick={this.handleStacktracePreviewClick}>
          <StacktraceContent data={stacktrace} expandFirstFrame={false} includeSystemFrames={((_a = stacktrace.frames) !== null && _a !== void 0 ? _a : []).every(function (frame) { return !frame.inApp; })} platform={((_b = event.platform) !== null && _b !== void 0 ? _b : 'other')} newestFirst={isStacktraceNewestFirst()} event={event} isHoverPreviewed/>
        </div>);
        }
        return null;
    };
    StacktracePreview.prototype.render = function () {
        var _a = this.props, children = _a.children, organization = _a.organization, disablePreview = _a.disablePreview;
        if (!organization.features.includes('stacktrace-hover-preview') || disablePreview) {
            return children;
        }
        return (<span onMouseEnter={this.fetchData}>
        <StyledHovercard body={this.renderHovercardBody()} position="right" modifiers={{
            flip: {
                enabled: false,
            },
            preventOverflow: {
                padding: 20,
                enabled: true,
                boundariesElement: 'viewport',
            },
        }}>
          {children}
        </StyledHovercard>
      </span>);
    };
    return StacktracePreview;
}(React.Component));
var StyledHovercard = styled(Hovercard)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 700px;\n\n  ", " {\n    padding: 0;\n    max-height: 300px;\n    overflow-y: auto;\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n\n  .traceback {\n    margin-bottom: 0;\n    border: 0;\n    box-shadow: none;\n  }\n\n  .loading .loading-indicator {\n    /**\n   * Overriding the .less file - for default 64px loader we have the width of border set to 6px\n   * For 48px we therefore need 4.5px to keep the same thickness ratio\n   */\n    border-width: 4.5px;\n  }\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  width: 700px;\n\n  ", " {\n    padding: 0;\n    max-height: 300px;\n    overflow-y: auto;\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n\n  .traceback {\n    margin-bottom: 0;\n    border: 0;\n    box-shadow: none;\n  }\n\n  .loading .loading-indicator {\n    /**\n   * Overriding the .less file - for default 64px loader we have the width of border set to 6px\n   * For 48px we therefore need 4.5px to keep the same thickness ratio\n   */\n    border-width: 4.5px;\n  }\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), Body, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.breakpoints[2]; });
var NoStackTraceWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  padding: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 80px;\n"], ["\n  color: ", ";\n  padding: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 80px;\n"])), function (p) { return p.theme.gray400; }, space(1.5));
export default withApi(StacktracePreview);
var templateObject_1, templateObject_2;
//# sourceMappingURL=stacktracePreview.jsx.map