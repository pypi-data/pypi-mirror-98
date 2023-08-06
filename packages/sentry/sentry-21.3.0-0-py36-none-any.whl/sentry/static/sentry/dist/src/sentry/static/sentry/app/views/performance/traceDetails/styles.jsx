import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { IconChevron } from 'app/icons';
import space from 'app/styles/space';
export { ConnectorBar, DividerLine, DividerLineGhostContainer, DurationPill, SpanBarRectangle as TransactionBarRectangle, SpanBarTitle as TransactionBarTitle, SpanBarTitleContainer as TransactionBarTitleContainer, SpanRowCell as TransactionRowCell, SpanRowCellContainer as TransactionRowCellContainer, SpanTreeConnector as TransactionTreeConnector, SpanTreeToggler as TransactionTreeToggle, SpanTreeTogglerContainer as TransactionTreeToggleContainer, } from 'app/components/events/interfaces/spans/spanBar';
export { SPAN_ROW_HEIGHT as TRANSACTION_ROW_HEIGHT, SPAN_ROW_PADDING as TRANSACTION_ROW_PADDING, SpanRow as TransactionRow, } from 'app/components/events/interfaces/spans/styles';
export var TraceViewContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"], ["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"])));
export var StyledIconChevron = styled(IconChevron)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 7px;\n  margin-left: ", ";\n"], ["\n  width: 7px;\n  margin-left: ", ";\n"])), space(0.25));
var templateObject_1, templateObject_2;
//# sourceMappingURL=styles.jsx.map