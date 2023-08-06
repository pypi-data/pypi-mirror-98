import { __extends, __read, __spread } from "tslib";
import React from 'react';
import TransactionBar from './transactionBar';
var TransactionGroup = /** @class */ (function (_super) {
    __extends(TransactionGroup, _super);
    function TransactionGroup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isExpanded: true,
        };
        _this.toggleExpandedState = function () {
            _this.setState(function (_a) {
                var isExpanded = _a.isExpanded;
                return ({ isExpanded: !isExpanded });
            });
        };
        return _this;
    }
    TransactionGroup.prototype.render = function () {
        var _a = this.props, index = _a.index, continuingDepths = _a.continuingDepths, isLast = _a.isLast, transaction = _a.transaction, traceInfo = _a.traceInfo;
        var isExpanded = this.state.isExpanded;
        var children = transaction.children;
        return (<React.Fragment>
        <TransactionBar index={index} transaction={transaction} traceInfo={traceInfo} continuingDepths={continuingDepths} isLast={isLast} isExpanded={isExpanded} toggleExpandedState={this.toggleExpandedState}/>
        {isExpanded &&
            children.map(function (child, idx) {
                var isLastChild = idx === children.length - 1;
                var hasChildren = child.children.length > 0;
                var newContinuingDepths = !isLastChild && hasChildren
                    ? __spread(continuingDepths, [transaction.generation]) : __spread(continuingDepths);
                // TODO(tonyx): figure out the index
                return (<TransactionGroup key={child.event_id} transaction={child} traceInfo={traceInfo} isLast={isLastChild} continuingDepths={newContinuingDepths}/>);
            })}
      </React.Fragment>);
    };
    TransactionGroup.defaultProps = {
        index: 0,
        isLast: true,
        continuingDepths: [],
    };
    return TransactionGroup;
}(React.Component));
export default TransactionGroup;
//# sourceMappingURL=transactionGroup.jsx.map