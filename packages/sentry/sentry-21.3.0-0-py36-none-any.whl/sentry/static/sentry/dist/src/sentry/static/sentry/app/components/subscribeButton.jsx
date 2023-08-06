import { __extends } from "tslib";
import React from 'react';
import Button from 'app/components/button';
import { IconBell } from 'app/icons';
import { t } from 'app/locale';
var SubscribeButton = /** @class */ (function (_super) {
    __extends(SubscribeButton, _super);
    function SubscribeButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SubscribeButton.prototype.render = function () {
        var _a = this.props, size = _a.size, isSubscribed = _a.isSubscribed, onClick = _a.onClick, disabled = _a.disabled;
        var icon = <IconBell color={isSubscribed ? 'blue300' : undefined}/>;
        return (<Button size={size} icon={icon} onClick={onClick} disabled={disabled}>
        {isSubscribed ? t('Unsubscribe') : t('Subscribe')}
      </Button>);
    };
    return SubscribeButton;
}(React.Component));
export default SubscribeButton;
//# sourceMappingURL=subscribeButton.jsx.map