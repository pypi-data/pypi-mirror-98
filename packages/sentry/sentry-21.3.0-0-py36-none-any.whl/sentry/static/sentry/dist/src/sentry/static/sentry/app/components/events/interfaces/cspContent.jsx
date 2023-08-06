import { __extends } from "tslib";
import React from 'react';
import KeyValueList from 'app/components/events/interfaces/keyValueList/keyValueList';
var CSPContent = /** @class */ (function (_super) {
    __extends(CSPContent, _super);
    function CSPContent() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CSPContent.prototype.render = function () {
        var data = this.props.data;
        return (<div>
        <h4>
          <span>{data.effective_directive}</span>
        </h4>
        <KeyValueList data={Object.entries(data)} isContextData/>
      </div>);
    };
    return CSPContent;
}(React.Component));
export default CSPContent;
//# sourceMappingURL=cspContent.jsx.map