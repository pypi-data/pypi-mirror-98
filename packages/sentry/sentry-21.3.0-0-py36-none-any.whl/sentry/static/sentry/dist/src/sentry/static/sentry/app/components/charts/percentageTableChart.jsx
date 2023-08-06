import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { Link } from 'react-router';
import isPropValid from '@emotion/is-prop-valid';
import styled from '@emotion/styled';
import classNames from 'classnames';
import PropTypes from 'prop-types';
import TableChart from 'app/components/charts/tableChart';
import Count from 'app/components/count';
import { PanelItem } from 'app/components/panels';
import { IconChevron } from 'app/icons';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
var Delta = function (_a) {
    var current = _a.current, previous = _a.previous, className = _a.className;
    if (typeof previous === 'undefined') {
        return null;
    }
    var changePercent = Math.round((Math.abs(current - previous) / previous) * 100);
    var direction = !changePercent ? 0 : current - previous;
    return (<StyledDelta direction={direction} className={className}>
      {!!direction && (<IconChevron direction={direction > 0 ? 'up' : 'down'} size="10px"/>)}
      {changePercent !== 0 ? changePercent + "%" : <span>&mdash;</span>}
    </StyledDelta>);
};
Delta.propTypes = {
    current: PropTypes.number,
    previous: PropTypes.number,
};
var StyledDelta = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: 0 ", ";\n  margin-right: ", ";\n  font-size: ", ";\n  color: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: 0 ", ";\n  margin-right: ", ";\n  font-size: ", ";\n  color: ",
    ";\n"])), space(0.25), space(0.5), function (p) { return p.theme.fontSizeSmall; }, function (p) {
    return p.direction > 0
        ? p.theme.green300
        : p.direction < 0
            ? p.theme.red300
            : p.theme.gray300;
});
var PercentageTableChart = /** @class */ (function (_super) {
    __extends(PercentageTableChart, _super);
    function PercentageTableChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRowClick = function (obj, e) {
            var onRowClick = _this.props.onRowClick;
            onRowClick(obj, e);
        };
        return _this;
    }
    PercentageTableChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, rowClassName = _a.rowClassName, headerClassName = _a.headerClassName, getRowLink = _a.getRowLink, title = _a.title, countTitle = _a.countTitle, extraTitle = _a.extraTitle, data = _a.data;
        return (<TableChart data={data.map(function (_a) {
            var value = _a.value, lastValue = _a.lastValue, name = _a.name, percentage = _a.percentage;
            return [
                <Name key="name">{name}</Name>,
                <CountColumn key="count">
            <Delta current={value} previous={lastValue}/>
            <Count value={value}/>
          </CountColumn>,
                <React.Fragment key="bar">
            <BarWrapper>
              <Bar width={percentage}/>
            </BarWrapper>
            <Percentage>{percentage}%</Percentage>
          </React.Fragment>,
            ];
        })} renderRow={function (_a) {
            var items = _a.items, rowIndex = _a.rowIndex;
            return (<Row dataRowClassName={rowClassName} headerRowClassName={headerClassName} getRowLink={getRowLink} onClick={_this.handleRowClick} data={data} rowIndex={rowIndex}>
            <NameAndCountContainer>
              {items[0]}
              <div>{items[1]}</div>
            </NameAndCountContainer>
            <PercentageContainer>
              <PercentageLabel>{items[2]}</PercentageLabel>
              {items[3]}
            </PercentageContainer>
          </Row>);
        }}>
        {function (_a) {
            var renderRow = _a.renderRow, renderBody = _a.renderBody, props = __rest(_a, ["renderRow", "renderBody"]);
            return (<TableChartWrapper>
            <TableHeader>
              {renderRow(__assign({ isTableHeader: true, items: [title, countTitle, t('Percentage'), extraTitle], rowIndex: -1 }, props))}
            </TableHeader>
            {renderBody(__assign({ renderRow: renderRow }, props))}
          </TableChartWrapper>);
        }}
      </TableChart>);
    };
    PercentageTableChart.propTypes = {
        // Main title (left most column) should
        title: PropTypes.node,
        // Label for the "count" title
        countTitle: PropTypes.node,
        extraTitle: PropTypes.node,
        onRowClick: PropTypes.func,
        // Class name for header
        headerClassName: PropTypes.string,
        // Class name for rows
        rowClassName: PropTypes.string,
        // If this is a function and returns a truthy value, then the row will be a link
        // to the return value of this function
        getRowLink: PropTypes.func,
        data: PropTypes.arrayOf(PropTypes.shape({
            name: PropTypes.node,
            percentage: PropTypes.number,
            value: PropTypes.number,
            lastValue: PropTypes.number,
        })),
    };
    PercentageTableChart.defaultProps = {
        title: '',
        countTitle: t('Count'),
        extraTitle: null,
        onRowClick: function () { },
    };
    return PercentageTableChart;
}(React.Component));
var Row = styled(function RowComponent(_a) {
    var headerRowClassName = _a.headerRowClassName, dataRowClassName = _a.dataRowClassName, className = _a.className, data = _a.data, getRowLink = _a.getRowLink, rowIndex = _a.rowIndex, onClick = _a.onClick, children = _a.children;
    var isLink = typeof getRowLink === 'function' && rowIndex > -1;
    var linkPath = isLink && getRowLink(data[rowIndex]);
    var Component = isLink ? Link : 'div';
    var rowProps = __assign(__assign({ className: classNames(className, rowIndex > -1 && dataRowClassName, rowIndex === -1 && headerRowClassName), children: children }, (linkPath && {
        to: linkPath,
    })), (!isLink &&
        typeof onClick === 'function' && {
        onClick: function (e) { return onClick(data[rowIndex], e); },
    }));
    return <Component {...rowProps}/>;
})(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  ", ";\n  font-size: 0.9em;\n"], ["\n  display: flex;\n  flex: 1;\n  ", ";\n  font-size: 0.9em;\n"])), function (p) { return p.rowIndex > -1 && 'cursor: pointer'; });
var FlexContainers = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"])));
var NameAndCountContainer = styled(FlexContainers)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex-shrink: 0;\n  margin-right: ", ";\n  width: 50%;\n"], ["\n  flex-shrink: 0;\n  margin-right: ", ";\n  width: 50%;\n"])), space(2));
var PercentageContainer = styled(FlexContainers)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  width: 50%;\n"], ["\n  width: 50%;\n"])));
var PercentageLabel = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"])));
var BarWrapper = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  flex: 1;\n  margin-right: ", ";\n  background-color: ", ";\n"], ["\n  flex: 1;\n  margin-right: ", ";\n  background-color: ", ";\n"])), space(1), function (p) { return p.theme.backgroundSecondary; });
var Percentage = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  flex-shrink: 0;\n  text-align: right;\n  width: 60px;\n"], ["\n  flex-shrink: 0;\n  text-align: right;\n  width: 60px;\n"])));
var Bar = styled('div', { shouldForwardProp: isPropValid })(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  flex: 1;\n  width: ", "%;\n  background-color: ", ";\n  height: 12px;\n  border-radius: 2px;\n"], ["\n  flex: 1;\n  width: ", "%;\n  background-color: ", ";\n  height: 12px;\n  border-radius: 2px;\n"])), function (p) { return p.width; }, function (p) { return p.theme.border; });
var Name = styled('span')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
var CountColumn = styled(Name)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-left: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-left: ", ";\n"])), space(0.5));
var TableHeader = styled(PanelItem)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  color: ", ";\n  padding: ", ";\n"], ["\n  color: ", ";\n  padding: ", ";\n"])), function (p) { return p.theme.gray300; }, space(1));
var TableChartWrapper = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  margin-bottom: 0;\n  padding: 0 ", ";\n\n  /* Fit to container dimensions */\n  width: 100%;\n  height: 100%;\n  display: flex;\n  flex-direction: column;\n\n  ", " {\n    padding: ", ";\n  }\n"], ["\n  margin-bottom: 0;\n  padding: 0 ", ";\n\n  /* Fit to container dimensions */\n  width: 100%;\n  height: 100%;\n  display: flex;\n  flex-direction: column;\n\n  ", " {\n    padding: ", ";\n  }\n"])), space(2), PanelItem, space(1));
export default PercentageTableChart;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13;
//# sourceMappingURL=percentageTableChart.jsx.map