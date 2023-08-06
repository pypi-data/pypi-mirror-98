import { __assign, __extends } from "tslib";
import React from 'react';
import * as queryString from 'query-string';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
var AddIntegration = /** @class */ (function (_super) {
    __extends(AddIntegration, _super);
    function AddIntegration() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.dialog = null;
        _this.openDialog = function (urlParams) {
            trackIntegrationEvent('integrations.installation_start', __assign({ integration: _this.props.provider.key, integration_type: 'first_party' }, _this.props.analyticsParams), _this.props.organization);
            var name = 'sentryAddIntegration';
            var _a = _this.props.provider.setupDialog, url = _a.url, width = _a.width, height = _a.height;
            var _b = _this.computeCenteredWindow(width, height), left = _b.left, top = _b.top;
            var query = __assign({}, urlParams);
            if (_this.props.account) {
                query.account = _this.props.account;
            }
            if (_this.props.modalParams) {
                query = __assign(__assign({}, query), _this.props.modalParams);
            }
            var installUrl = url + "?" + queryString.stringify(query);
            var opts = "scrollbars=yes,width=" + width + ",height=" + height + ",top=" + top + ",left=" + left;
            _this.dialog = window.open(installUrl, name, opts);
            _this.dialog && _this.dialog.focus();
        };
        _this.didReceiveMessage = function (message) {
            if (message.origin !== document.location.origin) {
                return;
            }
            if (message.source !== _this.dialog) {
                return;
            }
            var _a = message.data, success = _a.success, data = _a.data;
            _this.dialog = null;
            if (!success) {
                addErrorMessage(data.error);
                return;
            }
            if (!data) {
                return;
            }
            trackIntegrationEvent('integrations.installation_complete', __assign({ integration: _this.props.provider.key, integration_type: 'first_party' }, _this.props.analyticsParams), _this.props.organization);
            addSuccessMessage(t('%s added', _this.props.provider.name));
            _this.props.onInstall(data);
        };
        return _this;
    }
    AddIntegration.prototype.componentDidMount = function () {
        window.addEventListener('message', this.didReceiveMessage);
    };
    AddIntegration.prototype.componentWillUnmount = function () {
        window.removeEventListener('message', this.didReceiveMessage);
        this.dialog && this.dialog.close();
    };
    AddIntegration.prototype.computeCenteredWindow = function (width, height) {
        //Taken from: https://stackoverflow.com/questions/4068373/center-a-popup-window-on-screen
        var screenLeft = window.screenLeft !== undefined ? window.screenLeft : window.screenX;
        var screenTop = window.screenTop !== undefined ? window.screenTop : window.screenY;
        var innerWidth = window.innerWidth
            ? window.innerWidth
            : document.documentElement.clientWidth
                ? document.documentElement.clientWidth
                : screen.width;
        var innerHeight = window.innerHeight
            ? window.innerHeight
            : document.documentElement.clientHeight
                ? document.documentElement.clientHeight
                : screen.height;
        var left = innerWidth / 2 - width / 2 + screenLeft;
        var top = innerHeight / 2 - height / 2 + screenTop;
        return { left: left, top: top };
    };
    AddIntegration.prototype.render = function () {
        return this.props.children(this.openDialog);
    };
    return AddIntegration;
}(React.Component));
export default AddIntegration;
//# sourceMappingURL=addIntegration.jsx.map