import { __extends } from "tslib";
import React from 'react';
import * as DividerHandlerManager from 'app/components/events/interfaces/spans/dividerHandlerManager';
import { Panel } from 'app/components/panels';
import { TraceViewContainer } from './styles';
import TransactionGroup from './transactionGroup';
var TraceView = /** @class */ (function (_super) {
    __extends(TraceView, _super);
    function TraceView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.traceViewRef = React.createRef();
        return _this;
    }
    TraceView.prototype.render = function () {
        var _a = this.props, trace = _a.trace, traceInfo = _a.traceInfo;
        return (<Panel>
        <DividerHandlerManager.Provider interactiveLayerRef={this.traceViewRef}>
          <TraceViewContainer ref={this.traceViewRef}>
            <TransactionGroup transaction={trace} traceInfo={traceInfo}/>
          </TraceViewContainer>
        </DividerHandlerManager.Provider>
      </Panel>);
    };
    return TraceView;
}(React.Component));
export default TraceView;
//# sourceMappingURL=traceView.jsx.map