import { __extends } from "tslib";
import React from 'react';
// This is react-router v4 <Redirect to="path/" /> component to allow things
// to be declarative.
var Redirect = /** @class */ (function (_super) {
    __extends(Redirect, _super);
    function Redirect() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Redirect.prototype.componentDidMount = function () {
        this.props.router.replace(this.props.to);
    };
    Redirect.prototype.render = function () {
        return null;
    };
    return Redirect;
}(React.Component));
export default Redirect;
//# sourceMappingURL=redirect.jsx.map