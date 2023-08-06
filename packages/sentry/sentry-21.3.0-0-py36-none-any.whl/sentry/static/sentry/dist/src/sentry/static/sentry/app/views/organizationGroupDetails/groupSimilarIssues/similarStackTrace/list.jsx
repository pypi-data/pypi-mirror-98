import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody } from 'app/components/panels';
import SimilarSpectrum from 'app/components/similarSpectrum';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Item from './item';
import Toolbar from './toolbar';
var List = /** @class */ (function (_super) {
    __extends(List, _super);
    function List() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showAllItems: false,
        };
        _this.renderEmpty = function () { return (<Panel>
      <PanelBody>
        <EmptyStateWarning small withIcon={false}>
          {t('No issues with a similar stack trace have been found.')}
        </EmptyStateWarning>
      </PanelBody>
    </Panel>); };
        _this.handleShowAll = function () {
            _this.setState({ showAllItems: true });
        };
        return _this;
    }
    List.prototype.render = function () {
        var _a = this.props, orgId = _a.orgId, groupId = _a.groupId, project = _a.project, items = _a.items, filteredItems = _a.filteredItems, pageLinks = _a.pageLinks, onMerge = _a.onMerge, v2 = _a.v2;
        var showAllItems = this.state.showAllItems;
        var hasHiddenItems = !!filteredItems.length;
        var hasResults = items.length > 0 || hasHiddenItems;
        var itemsWithFiltered = items.concat((showAllItems && filteredItems) || []);
        if (!hasResults) {
            return this.renderEmpty();
        }
        return (<React.Fragment>
        <Header>
          <SimilarSpectrum />
        </Header>

        <Panel>
          <Toolbar v2={v2} onMerge={onMerge}/>

          <PanelBody>
            {itemsWithFiltered.map(function (item) { return (<Item key={item.issue.id} orgId={orgId} v2={v2} groupId={groupId} project={project} {...item}/>); })}

            {hasHiddenItems && !showAllItems && (<Footer>
                <Button onClick={this.handleShowAll}>
                  {t('Show %s issues below threshold', filteredItems.length)}
                </Button>
              </Footer>)}
          </PanelBody>
        </Panel>
        <Pagination pageLinks={pageLinks}/>
      </React.Fragment>);
    };
    List.defaultProps = {
        filteredItems: [],
    };
    return List;
}(React.Component));
export default List;
var Header = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  margin-bottom: ", ";\n"])), space(1));
var Footer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  justify-content: center;\n  padding: ", ";\n"])), space(1.5));
var templateObject_1, templateObject_2;
//# sourceMappingURL=list.jsx.map