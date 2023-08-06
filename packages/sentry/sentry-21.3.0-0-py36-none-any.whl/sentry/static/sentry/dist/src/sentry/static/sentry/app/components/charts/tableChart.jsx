import { __assign, __extends, __makeTemplateObject, __read, __rest, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import { Panel, PanelHeader, PanelItem } from 'app/components/panels';
var TableChartComponent = /** @class */ (function (_super) {
    __extends(TableChartComponent, _super);
    function TableChartComponent() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(TableChartComponent, "defaultProps", {
        get: function () {
            // Default renderer for Table Header
            var defaultRenderTableHeader = function (_a) {
                var headers = _a.headers, headerProps = _a.headerProps, renderRow = _a.renderRow, rowTotalLabel = _a.rowTotalLabel, showRowTotal = _a.showRowTotal, props = __rest(_a, ["headers", "headerProps", "renderRow", "rowTotalLabel", "showRowTotal"]);
                var headersWithTotalColumn = __spread((headers || []), (showRowTotal ? [rowTotalLabel] : []));
                return (<PanelHeader {...headerProps}>
          {renderRow(__assign({ isTableHeader: true, items: headersWithTotalColumn, rowIndex: -1, showRowTotal: showRowTotal }, props))}
        </PanelHeader>);
            };
            // Default renderer for Table Body (all the data rows)
            var defaultRenderBody = function (_a) {
                var widths = _a.widths, data = _a.data, dataTotals = _a.dataTotals, dataMaybeWithTotals = _a.dataMaybeWithTotals, renderRow = _a.renderRow, shadeRowPercentage = _a.shadeRowPercentage, showRowTotal = _a.showRowTotal, bodyHeight = _a.bodyHeight, props = __rest(_a, ["widths", "data", "dataTotals", "dataMaybeWithTotals", "renderRow", "shadeRowPercentage", "showRowTotal", "bodyHeight"]);
                return (<TableBody height={bodyHeight}>
        {dataMaybeWithTotals.map(function (row, rowIndex) {
                    var lastRowIndex = dataMaybeWithTotals.length - 1;
                    var isLastRow = rowIndex === lastRowIndex;
                    var showBar = !isLastRow && shadeRowPercentage;
                    // rowTotals does not include the grand total of data
                    var rowTotal = showRowTotal && rowIndex < data.length
                        ? [dataTotals.rowTotals[rowIndex]]
                        : [];
                    return (<TableChartRow key={rowIndex} showBar={showBar} value={dataTotals.rowTotals[rowIndex]} total={dataTotals.total} widths={widths}>
              {renderRow(__assign(__assign({ css: { zIndex: showBar ? '2' : undefined } }, props), { data: data,
                        widths: widths, items: __spread(row, rowTotal), rowIndex: rowIndex,
                        showRowTotal: showRowTotal }))}
            </TableChartRow>);
                })}
      </TableBody>);
            };
            // Default renderer for ALL rows (including header + body so that both can share the same DOM structure + styles)
            var defaultRenderRow = function (_a) {
                var dataStartIndex = _a.dataStartIndex, _css = _a.css, items = _a.items, _rowHeaders = _a.rowHeaders, _rowData = _a.rowData, isTableHeader = _a.isTableHeader, rowIndex = _a.rowIndex, renderCell = _a.renderCell, showRowTotal = _a.showRowTotal, rowTotalWidth = _a.rowTotalWidth, widths = _a.widths, props = __rest(_a, ["dataStartIndex", "css", "items", "rowHeaders", "rowData", "isTableHeader", "rowIndex", "renderCell", "showRowTotal", "rowTotalWidth", "widths"]);
                return (<Row>
        {items &&
                    items.slice(0, dataStartIndex).map(function (rowHeaderValue, columnIndex) {
                        return renderCell(__assign({ isTableHeader: isTableHeader, isHeader: true, value: rowHeaderValue, columnIndex: columnIndex,
                            rowIndex: rowIndex, width: columnIndex < widths.length
                                ? widths[columnIndex]
                                : showRowTotal
                                    ? rowTotalWidth
                                    : null, showRowTotal: showRowTotal }, props));
                    })}

        <DataGroup>
          {items &&
                    items.slice(dataStartIndex).map(function (rowDataValue, columnIndex) {
                        var index = columnIndex + dataStartIndex;
                        var renderCellProps = __assign({ isTableHeader: isTableHeader, value: rowDataValue, columnIndex: index, rowIndex: rowIndex, width: index < widths.length
                                ? widths[index]
                                : showRowTotal
                                    ? rowTotalWidth
                                    : null, justify: 'right', showRowTotal: showRowTotal }, props);
                        return renderCell(renderCellProps);
                    })}
        </DataGroup>
      </Row>);
            };
            // Default renderer for ALL cells
            var defaultRenderCell = function (p) {
                var isTableHeader = p.isTableHeader, isHeader = p.isHeader, justify = p.justify, width = p.width, rowIndex = p.rowIndex, columnIndex = p.columnIndex, renderTableHeaderCell = p.renderTableHeaderCell, renderHeaderCell = p.renderHeaderCell, renderDataCell = p.renderDataCell;
                return (<Cell justify={justify} width={width} key={rowIndex + "-" + columnIndex}>
          {isTableHeader
                    ? renderTableHeaderCell(p)
                    : isHeader
                        ? renderHeaderCell(p)
                        : renderDataCell(p)}
        </Cell>);
            };
            var defaultRenderDataCell = function (_a) {
                var value = _a.value;
                return value;
            };
            var defaultRenderHeaderCell = defaultRenderDataCell;
            var defaultRenderTableHeaderCell = defaultRenderHeaderCell;
            return {
                dataStartIndex: 1,
                getValue: function (i) { return i; },
                renderTableHeader: defaultRenderTableHeader,
                renderBody: defaultRenderBody,
                renderRow: defaultRenderRow,
                renderCell: defaultRenderCell,
                renderDataCell: defaultRenderDataCell,
                renderHeaderCell: defaultRenderHeaderCell,
                renderTableHeaderCell: defaultRenderTableHeaderCell,
                columnTotalLabel: 'Total',
                rowTotalLabel: 'Total',
                rowTotalWidth: 120,
            };
        },
        enumerable: false,
        configurable: true
    });
    // TODO(billy): memoize?
    TableChartComponent.prototype.getTotals = function (rows) {
        if (!rows) {
            return [];
        }
        var _a = this.props, getValue = _a.getValue, dataStartIndex = _a.dataStartIndex;
        var reduceSum = function (sum, val) { return (sum += getValue(val)); };
        var rowTotals = rows.map(function (row) { return row.slice(dataStartIndex).reduce(reduceSum, 0); });
        var columnTotals = rows.length
            ? rows[0]
                .slice(dataStartIndex)
                .map(function (_r, currentColumn) {
                return rows.reduce(function (sum, row) { return (sum += getValue(row[currentColumn + dataStartIndex])); }, 0);
            })
            : [];
        var total = columnTotals.reduce(reduceSum, 0);
        rowTotals.push(total);
        return {
            rowTotals: rowTotals,
            columnTotals: columnTotals,
            total: total,
        };
    };
    TableChartComponent.prototype.getDataWithTotals = function (dataTotals) {
        var _a = this.props, data = _a.data, dataStartIndex = _a.dataStartIndex, showRowTotal = _a.showRowTotal, showColumnTotal = _a.showColumnTotal, columnTotalLabel = _a.columnTotalLabel;
        if (!data) {
            return [];
        }
        var totalRow = showColumnTotal
            ? [
                __spread([
                    // Label for Total Row
                    columnTotalLabel
                ], __spread(Array(dataStartIndex - 1)).map(function () { return ''; }), dataTotals.columnTotals, (showRowTotal ? [dataTotals.total] : [])),
            ]
            : [];
        return __spread(data, totalRow);
    };
    TableChartComponent.prototype.render = function () {
        var _a = this.props, className = _a.className, children = _a.children, data = _a.data, dataStartIndex = _a.dataStartIndex, getValue = _a.getValue, showRowTotal = _a.showRowTotal, showColumnTotal = _a.showColumnTotal, shadeRowPercentage = _a.shadeRowPercentage, renderTableHeader = _a.renderTableHeader, renderBody = _a.renderBody, widths = _a.widths, props = __rest(_a, ["className", "children", "data", "dataStartIndex", "getValue", "showRowTotal", "showColumnTotal", "shadeRowPercentage", "renderTableHeader", "renderBody", "widths"]);
        // If we need to calculate totals...
        var dataTotals = showRowTotal || showColumnTotal || shadeRowPercentage
            ? this.getTotals(data)
            : {
                rowTotals: [],
                columnTotals: [],
            };
        var dataMaybeWithTotals = this.getDataWithTotals(dataTotals);
        // For better render customization
        var isRenderProp = typeof children === 'function';
        var renderProps = __assign({ data: data,
            dataTotals: dataTotals,
            dataMaybeWithTotals: dataMaybeWithTotals,
            dataStartIndex: dataStartIndex,
            getValue: getValue,
            showRowTotal: showRowTotal,
            showColumnTotal: showColumnTotal,
            shadeRowPercentage: shadeRowPercentage,
            widths: widths,
            renderBody: renderBody,
            renderTableHeader: renderTableHeader }, props);
        if (isRenderProp) {
            return children(renderProps);
        }
        return (<Panel className={className}>
        {renderTableHeader(renderProps)}
        {renderBody(renderProps)}
      </Panel>);
    };
    TableChartComponent.propTypes = {
        data: PropTypes.arrayOf(PropTypes.any),
        /**
         * The column index where your data starts.
         * This is used to calculate totals.
         *
         * Will not work if you have mixed string/number columns
         */
        dataStartIndex: PropTypes.number,
        widths: PropTypes.arrayOf(PropTypes.number),
        // Height of body
        bodyHeight: PropTypes.string,
        getValue: PropTypes.func,
        renderTableHeader: PropTypes.func,
        renderBody: PropTypes.func,
        renderHeaderCell: PropTypes.func,
        renderDataCell: PropTypes.func,
        shadeRowPercentage: PropTypes.bool,
        showRowTotal: PropTypes.bool,
        showColumnTotal: PropTypes.bool,
        rowTotalLabel: PropTypes.string,
        columnTotalLabel: PropTypes.string,
        // props to pass to PanelHeader
        headerProps: PropTypes.object,
    };
    return TableChartComponent;
}(React.Component));
export var TableChart = styled(TableChartComponent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
export default TableChart;
export var TableChartRow = styled(/** @class */ (function (_super) {
    __extends(TableChartRowComponent, _super);
    function TableChartRowComponent() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TableChartRowComponent.prototype.render = function () {
        var _a = this.props, className = _a.className, showBar = _a.showBar, total = _a.total, value = _a.value, children = _a.children;
        var barWidth = total > 0 && typeof value === 'number' ? Math.round((value / total) * 100) : 0;
        return (<PanelItem className={className}>
          {children}
          {showBar && <TableChartRowBar width={barWidth}/>}
        </PanelItem>);
    };
    return TableChartRowComponent;
}(React.Component)))(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  flex: 1;\n"], ["\n  position: relative;\n  flex: 1;\n"])));
/**
 * Shows relative percentage as width of bar inside of a table's row
 */
export var TableChartRowBar = styled(function (_a) {
    var _width = _a.width, props = __rest(_a, ["width"]);
    return <div {...props}/>;
})(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  left: 0;\n  right: ", "%;\n  background-color: ", ";\n  z-index: 1;\n"], ["\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  left: 0;\n  right: ", "%;\n  background-color: ", ";\n  z-index: 1;\n"])), function (p) { return 100 - p.width; }, function (p) { return p.theme.backgroundSecondary; });
export var Cell = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  z-index: 2;\n  display: block;\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n  ", ";\n  ", ";\n"], ["\n  z-index: 2;\n  display: block;\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n  ", ";\n  ", ";\n"])), function (p) { return (!p.width ? 'flex: 1' : ''); }, function (p) { return (p.justify === 'right' ? 'text-align: right' : ''); });
var DataGroup = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  flex-shrink: 0;\n"], ["\n  display: flex;\n  flex-shrink: 0;\n"])));
var Row = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  overflow: hidden;\n"], ["\n  display: flex;\n  flex: 1;\n  overflow: hidden;\n"])));
var TableBody = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  height: ", ";\n  flex-grow: 1;\n  overflow-y: auto;\n"], ["\n  height: ", ";\n  flex-grow: 1;\n  overflow-y: auto;\n"])), function (p) { return p.height; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=tableChart.jsx.map