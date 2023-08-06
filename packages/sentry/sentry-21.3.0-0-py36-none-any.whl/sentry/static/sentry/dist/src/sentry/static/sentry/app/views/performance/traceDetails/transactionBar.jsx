import { __extends } from "tslib";
import React from 'react';
import { withTheme } from 'emotion-theming';
import Count from 'app/components/count';
import * as DividerHandlerManager from 'app/components/events/interfaces/spans/dividerHandlerManager';
import { ConnectorBar, DividerLine, DividerLineGhostContainer, DurationPill, StyledIconChevron, TRANSACTION_ROW_HEIGHT, TransactionBarRectangle, TransactionBarTitle, TransactionBarTitleContainer, TransactionRow, TransactionRowCell, TransactionRowCellContainer, TransactionTreeConnector, TransactionTreeToggle, TransactionTreeToggleContainer, } from './styles';
import { getDurationDisplay, getHumanDuration, toPercent } from './utils';
var TOGGLE_BUTTON_MARGIN_RIGHT = 16;
var TOGGLE_BUTTON_MAX_WIDTH = 30;
export var TOGGLE_BORDER_BOX = TOGGLE_BUTTON_MAX_WIDTH + TOGGLE_BUTTON_MARGIN_RIGHT;
var MARGIN_LEFT = 0;
function getOffset(generation) {
    return generation * (TOGGLE_BORDER_BOX / 2) + MARGIN_LEFT;
}
var TransactionBar = /** @class */ (function (_super) {
    __extends(TransactionBar, _super);
    function TransactionBar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TransactionBar.prototype.getCurrentOffset = function () {
        var transaction = this.props.transaction;
        var generation = transaction.generation;
        return getOffset(generation);
    };
    TransactionBar.prototype.renderConnector = function (hasToggle) {
        var _a = this.props, continuingDepths = _a.continuingDepths, isExpanded = _a.isExpanded, isLast = _a.isLast, transaction = _a.transaction;
        var event_id = transaction.event_id, generation = transaction.generation;
        if (generation === 0) {
            if (hasToggle) {
                return (<ConnectorBar style={{ right: '16px', height: '10px', bottom: '-5px', top: 'auto' }} orphanBranch={false}/>);
            }
            return null;
        }
        var connectorBars = continuingDepths.map(function (depth) {
            if (generation - depth <= 1) {
                // If the difference is less than or equal to 1, then it means that the continued
                // bar is from its direct parent. In this case, do not render a connector bar
                // because the tree connector below will suffice.
                return null;
            }
            var left = -1 * getOffset(generation - depth - 1) - 1;
            return (<ConnectorBar style={{ left: left }} key={event_id + "-" + depth} orphanBranch={false}/>);
        });
        if (hasToggle && isExpanded) {
            connectorBars.push(<ConnectorBar style={{
                right: '16px',
                height: '10px',
                bottom: isLast ? "-" + TRANSACTION_ROW_HEIGHT / 2 + "px" : '0',
                top: 'auto',
            }} key={event_id + "-last"} orphanBranch={false}/>);
        }
        return (<TransactionTreeConnector isLast={isLast} hasToggler={hasToggle} orphanBranch={false} // TODO(tonyx): what does an orphan mean here?
        >
        {connectorBars}
      </TransactionTreeConnector>);
    };
    TransactionBar.prototype.renderToggle = function () {
        var _a = this.props, isExpanded = _a.isExpanded, transaction = _a.transaction, toggleExpandedState = _a.toggleExpandedState;
        var children = transaction.children, generation = transaction.generation;
        var left = this.getCurrentOffset();
        if (children.length <= 0) {
            return (<TransactionTreeToggleContainer style={{ left: left + "px" }}>
          {this.renderConnector(false)}
        </TransactionTreeToggleContainer>);
        }
        var isRoot = generation === 0;
        return (<TransactionTreeToggleContainer style={{ left: left + "px" }} hasToggler>
        {this.renderConnector(true)}
        <TransactionTreeToggle disabled={isRoot} isExpanded={isExpanded} onClick={function (event) {
            event.stopPropagation();
            if (isRoot) {
                return;
            }
            toggleExpandedState();
        }}>
          <Count value={children.length}/>
          {!isRoot && (<div>
              <StyledIconChevron direction={isExpanded ? 'up' : 'down'}/>
            </div>)}
        </TransactionTreeToggle>
      </TransactionTreeToggleContainer>);
    };
    TransactionBar.prototype.renderTitle = function () {
        var transaction = this.props.transaction;
        var left = this.getCurrentOffset();
        return (<TransactionBarTitleContainer>
        {this.renderToggle()}
        <TransactionBarTitle style={{
            left: left + "px",
            width: '100%',
        }}>
          <span>{transaction.transaction}</span>
        </TransactionBarTitle>
      </TransactionBarTitleContainer>);
    };
    TransactionBar.prototype.renderDivider = function (dividerHandlerChildrenProps) {
        var addDividerLineRef = dividerHandlerChildrenProps.addDividerLineRef;
        return (<DividerLine ref={addDividerLineRef()} style={{
            position: 'relative',
        }} onMouseEnter={function () {
            dividerHandlerChildrenProps.setHover(true);
        }} onMouseLeave={function () {
            dividerHandlerChildrenProps.setHover(false);
        }} onMouseOver={function () {
            dividerHandlerChildrenProps.setHover(true);
        }} onMouseDown={dividerHandlerChildrenProps.onDragStart} onClick={function (event) {
            // we prevent the propagation of the clicks from this component to prevent
            // the span detail from being opened.
            event.stopPropagation();
        }}/>);
    };
    TransactionBar.prototype.renderGhostDivider = function (dividerHandlerChildrenProps) {
        var dividerPosition = dividerHandlerChildrenProps.dividerPosition, addGhostDividerLineRef = dividerHandlerChildrenProps.addGhostDividerLineRef;
        return (<DividerLineGhostContainer style={{
            width: "calc(" + toPercent(dividerPosition) + " + 0.5px)",
            display: 'none',
        }}>
        <DividerLine ref={addGhostDividerLineRef()} style={{
            right: 0,
        }} className="hovering" onClick={function (event) {
            // the ghost divider line should not be interactive.
            // we prevent the propagation of the clicks from this component to prevent
            // the span detail from being opened.
            event.stopPropagation();
        }}/>
      </DividerLineGhostContainer>);
    };
    TransactionBar.prototype.renderRectangle = function () {
        var _a = this.props, transaction = _a.transaction, traceInfo = _a.traceInfo, theme = _a.theme;
        var palette = theme.charts.getColorPalette(traceInfo.maxGeneration);
        // Use 1 as the difference in the event that startTimestamp === endTimestamp
        var delta = Math.abs(traceInfo.endTimestamp - traceInfo.startTimestamp) || 1;
        var startPosition = Math.abs(transaction.start_timestamp - traceInfo.startTimestamp);
        var startPercentage = startPosition / delta;
        var duration = Math.abs(transaction.timestamp - transaction.start_timestamp);
        var widthPercentage = duration / delta;
        return (<TransactionBarRectangle spanBarHatch={false} style={{
            backgroundColor: palette[transaction.generation % palette.length],
            left: "clamp(0%, " + toPercent(startPercentage || 0) + ", calc(100% - 1px))",
            width: toPercent(widthPercentage || 0),
        }}>
        <DurationPill durationDisplay={getDurationDisplay({
            left: startPercentage,
            width: widthPercentage,
        })} showDetail={false} spanBarHatch={false}>
          {getHumanDuration(duration)}
        </DurationPill>
      </TransactionBarRectangle>);
    };
    TransactionBar.prototype.renderHeader = function (_a) {
        var dividerHandlerChildrenProps = _a.dividerHandlerChildrenProps;
        var index = this.props.index;
        var dividerPosition = dividerHandlerChildrenProps.dividerPosition;
        return (<TransactionRowCellContainer>
        <TransactionRowCell style={{
            width: "calc(" + toPercent(dividerPosition) + " - 0.5px)",
            paddingTop: 0,
        }}>
          {this.renderTitle()}
        </TransactionRowCell>
        {this.renderDivider(dividerHandlerChildrenProps)}
        <TransactionRowCell showStriping={index % 2 !== 0} style={{
            width: "calc(" + toPercent(1 - dividerPosition) + " - 0.5px)",
            paddingTop: 0,
        }}>
          {this.renderRectangle()}
        </TransactionRowCell>
        {this.renderGhostDivider(dividerHandlerChildrenProps)}
      </TransactionRowCellContainer>);
    };
    TransactionBar.prototype.render = function () {
        var _this = this;
        return (<TransactionRow visible>
        <DividerHandlerManager.Consumer>
          {function (dividerHandlerChildrenProps) {
            return _this.renderHeader({ dividerHandlerChildrenProps: dividerHandlerChildrenProps });
        }}
        </DividerHandlerManager.Consumer>
      </TransactionRow>);
    };
    return TransactionBar;
}(React.Component));
export default withTheme(TransactionBar);
//# sourceMappingURL=transactionBar.jsx.map