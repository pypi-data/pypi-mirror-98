import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { CreateAlertFromViewButton } from 'app/components/createAlertButton';
import DropdownControl from 'app/components/dropdownControl';
import Hovercard from 'app/components/hovercard';
import { IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import EventView from 'app/utils/discover/eventView';
import { getDiscoverLandingUrl } from 'app/utils/discover/urls';
import withApi from 'app/utils/withApi';
import withProjects from 'app/utils/withProjects';
import { setBannerHidden } from 'app/views/eventsV2/utils';
import InputControl from 'app/views/settings/components/forms/controls/input';
import { handleCreateQuery, handleDeleteQuery, handleUpdateQuery } from './utils';
var SavedQueryButtonGroup = /** @class */ (function (_super) {
    __extends(SavedQueryButtonGroup, _super);
    function SavedQueryButtonGroup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isNewQuery: true,
            isEditingQuery: false,
            queryName: '',
        };
        _this.onBlurInput = function (event) {
            var target = event.target;
            _this.setState({ queryName: target.value });
        };
        _this.onChangeInput = function (event) {
            var target = event.target;
            _this.setState({ queryName: target.value });
        };
        /**
         * There are two ways to create a query
         * 1) Creating a query from scratch and saving it
         * 2) Modifying an existing query and saving it
         */
        _this.handleCreateQuery = function (event) {
            event.preventDefault();
            event.stopPropagation();
            var _a = _this.props, api = _a.api, organization = _a.organization, eventView = _a.eventView;
            if (!_this.state.queryName) {
                return;
            }
            var nextEventView = eventView.clone();
            nextEventView.name = _this.state.queryName;
            // Checks if "Save as" button is clicked from a clean state, or it is
            // clicked while modifying an existing query
            var isNewQuery = !eventView.id;
            handleCreateQuery(api, organization, nextEventView, isNewQuery).then(function (savedQuery) {
                var view = EventView.fromSavedQuery(savedQuery);
                setBannerHidden(true);
                _this.setState({ queryName: '' });
                browserHistory.push(view.getResultsViewUrlTarget(organization.slug));
            });
        };
        _this.handleUpdateQuery = function (event) {
            event.preventDefault();
            event.stopPropagation();
            var _a = _this.props, api = _a.api, organization = _a.organization, eventView = _a.eventView, updateCallback = _a.updateCallback;
            handleUpdateQuery(api, organization, eventView).then(function (savedQuery) {
                var view = EventView.fromSavedQuery(savedQuery);
                _this.setState({ queryName: '' });
                browserHistory.push(view.getResultsViewUrlTarget(organization.slug));
                updateCallback();
            });
        };
        _this.handleDeleteQuery = function (event) {
            event.preventDefault();
            event.stopPropagation();
            var _a = _this.props, api = _a.api, organization = _a.organization, eventView = _a.eventView;
            handleDeleteQuery(api, organization, eventView).then(function () {
                browserHistory.push({
                    pathname: getDiscoverLandingUrl(organization),
                    query: {},
                });
            });
        };
        _this.handleCreateAlertSuccess = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'discover_v2.create_alert_clicked',
                eventName: 'Discoverv2: Create alert clicked',
                status: 'success',
                organization_id: organization.id,
                url: window.location.href,
            });
        };
        return _this;
    }
    SavedQueryButtonGroup.getDerivedStateFromProps = function (nextProps, prevState) {
        var nextEventView = nextProps.eventView, savedQuery = nextProps.savedQuery, savedQueryLoading = nextProps.savedQueryLoading;
        // For a new unsaved query
        if (!savedQuery) {
            return {
                isNewQuery: true,
                isEditingQuery: false,
                queryName: prevState.queryName || '',
            };
        }
        if (savedQueryLoading) {
            return prevState;
        }
        var savedEventView = EventView.fromSavedQuery(savedQuery);
        // Switching from a SavedQuery to another SavedQuery
        if (savedEventView.id !== nextEventView.id) {
            return {
                isNewQuery: false,
                isEditingQuery: false,
                queryName: '',
            };
        }
        // For modifying a SavedQuery
        var isEqualQuery = nextEventView.isEqualTo(savedEventView);
        return {
            isNewQuery: false,
            isEditingQuery: !isEqualQuery,
            // HACK(leedongwei): See comment at SavedQueryButtonGroup.onFocusInput
            queryName: prevState.queryName || '',
        };
    };
    SavedQueryButtonGroup.prototype.renderButtonSaveAs = function (disabled) {
        var queryName = this.state.queryName;
        /**
         * For a great UX, we should focus on `ButtonSaveInput` when `ButtonSave`
         * is clicked. However, `DropdownControl` wraps them in a FunctionComponent
         * which breaks `React.createRef`.
         */
        return (<DropdownControl alignRight menuWidth="220px" priority="default" buttonProps={{
            'aria-label': t('Save as'),
            showChevron: false,
            disabled: disabled,
        }} label={t('Save as') + "\u2026"}>
        <ButtonSaveDropDown onClick={SavedQueryButtonGroup.stopEventPropagation}>
          <ButtonSaveInput type="text" name="query_name" placeholder={t('Display name')} value={queryName || ''} onBlur={this.onBlurInput} onChange={this.onChangeInput} disabled={disabled}/>
          <Button onClick={this.handleCreateQuery} priority="primary" disabled={disabled || !this.state.queryName} style={{ width: '100%' }}>
            {t('Save')}
          </Button>
        </ButtonSaveDropDown>
      </DropdownControl>);
    };
    SavedQueryButtonGroup.prototype.renderButtonSave = function (disabled) {
        var _a = this.state, isNewQuery = _a.isNewQuery, isEditingQuery = _a.isEditingQuery;
        // Existing query that hasn't been modified.
        if (!isNewQuery && !isEditingQuery) {
            return (<Button disabled data-test-id="discover2-savedquery-button-saved">
          {t('Saved query')}
        </Button>);
        }
        // Existing query with edits, show save and save as.
        if (!isNewQuery && isEditingQuery) {
            return (<React.Fragment>
          <Button onClick={this.handleUpdateQuery} data-test-id="discover2-savedquery-button-update" disabled={disabled}>
            <IconUpdate />
            {t('Save Changes')}
          </Button>
          {this.renderButtonSaveAs(disabled)}
        </React.Fragment>);
        }
        // Is a new query enable saveas
        return this.renderButtonSaveAs(disabled);
    };
    SavedQueryButtonGroup.prototype.renderButtonDelete = function (disabled) {
        var isNewQuery = this.state.isNewQuery;
        if (isNewQuery) {
            return null;
        }
        return (<Button data-test-id="discover2-savedquery-button-delete" onClick={this.handleDeleteQuery} disabled={disabled} icon={<IconDelete />}/>);
    };
    SavedQueryButtonGroup.prototype.renderButtonCreateAlert = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects, onIncompatibleAlertQuery = _a.onIncompatibleAlertQuery;
        return (<CreateAlertFromViewButton eventView={eventView} organization={organization} projects={projects} onIncompatibleQuery={onIncompatibleAlertQuery} onSuccess={this.handleCreateAlertSuccess} referrer="discover" data-test-id="discover2-create-from-discover"/>);
    };
    SavedQueryButtonGroup.prototype.render = function () {
        var _this = this;
        var organization = this.props.organization;
        var renderDisabled = function (p) { return (<Hovercard body={<FeatureDisabled features={p.features} hideHelpToggle message={t('Discover queries are disabled')} featureName={t('Discover queries')}/>}>
        {p.children(p)}
      </Hovercard>); };
        var renderQueryButton = function (renderFunc) {
            return (<Feature organization={organization} features={['discover-query']} hookName="feature-disabled:discover-saved-query-create" renderDisabled={renderDisabled}>
          {function (_a) {
                var hasFeature = _a.hasFeature;
                return renderFunc(!hasFeature || _this.props.disabled);
            }}
        </Feature>);
        };
        return (<ResponsiveButtonBar gap={1}>
        {renderQueryButton(function (disabled) { return _this.renderButtonSave(disabled); })}
        <Feature organization={organization} features={['incidents']}>
          {function (_a) {
            var hasFeature = _a.hasFeature;
            return hasFeature && _this.renderButtonCreateAlert();
        }}
        </Feature>
        {renderQueryButton(function (disabled) { return _this.renderButtonDelete(disabled); })}
      </ResponsiveButtonBar>);
    };
    /**
     * Stop propagation for the input and container so people can interact with
     * the inputs in the dropdown.
     */
    SavedQueryButtonGroup.stopEventPropagation = function (event) {
        var capturedElements = ['LI', 'INPUT'];
        if (event.target instanceof Element &&
            capturedElements.includes(event.target.nodeName)) {
            event.preventDefault();
            event.stopPropagation();
        }
    };
    SavedQueryButtonGroup.defaultProps = {
        disabled: false,
    };
    return SavedQueryButtonGroup;
}(React.PureComponent));
var ResponsiveButtonBar = styled(ButtonBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-top: 0;\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-top: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var ButtonSaveDropDown = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  padding: ", ";\n  gap: ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  padding: ", ";\n  gap: ", ";\n"])), space(1), space(1));
var ButtonSaveInput = styled(InputControl)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  height: 40px;\n"], ["\n  height: 40px;\n"])));
var IconUpdate = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: inline-block;\n  width: 10px;\n  height: 10px;\n\n  margin-right: ", ";\n  border-radius: 5px;\n  background-color: ", ";\n"], ["\n  display: inline-block;\n  width: 10px;\n  height: 10px;\n\n  margin-right: ", ";\n  border-radius: 5px;\n  background-color: ", ";\n"])), space(0.75), function (p) { return p.theme.yellow300; });
export default withProjects(withApi(SavedQueryButtonGroup));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map