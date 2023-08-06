import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __rest, __spread } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import partition from 'lodash/partition';
import sortBy from 'lodash/sortBy';
import { addErrorMessage } from 'app/actionCreators/indicator';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import NotAvailable from 'app/components/notAvailable';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { CandidateDownloadStatus } from 'app/types/debugImage';
import theme from 'app/utils/theme';
import Address from '../address';
import Processings from '../debugImage/processings';
import { getFileName } from '../utils';
import Candidates from './candidates';
import { INTERNAL_SOURCE, INTERNAL_SOURCE_LOCATION } from './utils';
var DebugImageDetails = /** @class */ (function (_super) {
    __extends(DebugImageDetails, _super);
    function DebugImageDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (debugId) { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, projectId, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, projectId = _a.projectId;
                        this.setState({ loading: true });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + organization.slug + "/" + projectId + "/files/dsyms/?id=" + debugId, { method: 'DELETE' })];
                    case 2:
                        _c.sent();
                        this.fetchData();
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        addErrorMessage(t('An error occurred while deleting the debug file.'));
                        this.setState({ loading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    DebugImageDetails.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { debugFiles: [], builtinSymbolSources: [] });
    };
    DebugImageDetails.prototype.getUplodedDebugFiles = function (candidates) {
        return candidates.find(function (candidate) { return candidate.source === INTERNAL_SOURCE; });
    };
    DebugImageDetails.prototype.getEndpoints = function () {
        var _a;
        var _b = this.props, organization = _b.organization, projectId = _b.projectId, image = _b.image;
        if (!image) {
            return [];
        }
        var debug_id = image.debug_id, _c = image.candidates, candidates = _c === void 0 ? [] : _c;
        var builtinSymbolSources = (this.state || {}).builtinSymbolSources;
        var uploadedDebugFiles = this.getUplodedDebugFiles(candidates);
        var endpoints = [];
        if (uploadedDebugFiles) {
            endpoints.push([
                'debugFiles',
                "/projects/" + organization.slug + "/" + projectId + "/files/dsyms/?debug_id=" + debug_id,
                {
                    query: {
                        file_formats: !!((_a = organization.features) === null || _a === void 0 ? void 0 : _a.includes('android-mappings'))
                            ? ['breakpad', 'macho', 'elf', 'pe', 'pdb', 'sourcebundle']
                            : undefined,
                    },
                },
            ]);
        }
        if (!(builtinSymbolSources === null || builtinSymbolSources === void 0 ? void 0 : builtinSymbolSources.length) &&
            organization.features.includes('symbol-sources')) {
            endpoints.push(['builtinSymbolSources', '/builtin-symbol-sources/', {}]);
        }
        return endpoints;
    };
    DebugImageDetails.prototype.sortCandidates = function (candidates, unAppliedCandidates) {
        var _a = __read(partition(candidates, function (candidate) { return candidate.download.status === CandidateDownloadStatus.NO_PERMISSION; }), 2), noPermissionCandidates = _a[0], restNoPermissionCandidates = _a[1];
        var _b = __read(partition(restNoPermissionCandidates, function (candidate) { return candidate.download.status === CandidateDownloadStatus.MALFORMED; }), 2), malFormedCandidates = _b[0], restMalFormedCandidates = _b[1];
        var _c = __read(partition(restMalFormedCandidates, function (candidate) { return candidate.download.status === CandidateDownloadStatus.ERROR; }), 2), errorCandidates = _c[0], restErrorCandidates = _c[1];
        var _d = __read(partition(restErrorCandidates, function (candidate) { return candidate.download.status === CandidateDownloadStatus.OK; }), 2), okCandidates = _d[0], restOKCandidates = _d[1];
        var _e = __read(partition(restOKCandidates, function (candidate) { return candidate.download.status === CandidateDownloadStatus.DELETED; }), 2), deletedCandidates = _e[0], notFoundCandidates = _e[1];
        return __spread(sortBy(noPermissionCandidates, ['source_name', 'location']), sortBy(malFormedCandidates, ['source_name', 'location']), sortBy(errorCandidates, ['source_name', 'location']), sortBy(okCandidates, ['source_name', 'location']), sortBy(deletedCandidates, ['source_name', 'location']), sortBy(unAppliedCandidates, ['source_name', 'location']), sortBy(notFoundCandidates, ['source_name', 'location']));
    };
    DebugImageDetails.prototype.getCandidates = function () {
        var _a = this.state, debugFiles = _a.debugFiles, loading = _a.loading;
        var image = this.props.image;
        var _b = (image !== null && image !== void 0 ? image : {}).candidates, candidates = _b === void 0 ? [] : _b;
        if (!debugFiles || loading) {
            return candidates;
        }
        var imageCandidates = candidates.map(function (_a) {
            var location = _a.location, candidate = __rest(_a, ["location"]);
            return (__assign(__assign({}, candidate), { location: (location === null || location === void 0 ? void 0 : location.includes(INTERNAL_SOURCE_LOCATION)) ? location.split(INTERNAL_SOURCE_LOCATION)[1]
                    : location }));
        });
        // Check for unapplied candidates (debug files)
        var candidateLocations = new Set(imageCandidates.map(function (_a) {
            var location = _a.location;
            return location;
        }).filter(function (location) { return !!location; }));
        var unAppliedCandidates = debugFiles
            .filter(function (debugFile) { return !candidateLocations.has(debugFile.id); })
            .map(function (debugFile) { return ({
            download: {
                status: CandidateDownloadStatus.UNAPPLIED,
            },
            location: "" + INTERNAL_SOURCE_LOCATION + debugFile.id,
            source: INTERNAL_SOURCE,
            source_name: debugFile.objectName,
        }); });
        // Check for deleted candidates (debug files)
        var debugFileIds = new Set(debugFiles.map(function (debugFile) { return debugFile.id; }));
        var convertedCandidates = imageCandidates.map(function (candidate) {
            if (candidate.source === INTERNAL_SOURCE &&
                candidate.location &&
                !debugFileIds.has(candidate.location) &&
                candidate.download.status === CandidateDownloadStatus.OK) {
                return __assign(__assign({}, candidate), { download: __assign(__assign({}, candidate.download), { status: CandidateDownloadStatus.DELETED }) });
            }
            return candidate;
        });
        return this.sortCandidates(convertedCandidates, unAppliedCandidates);
    };
    DebugImageDetails.prototype.getDebugFilesSettingsLink = function () {
        var _a = this.props, organization = _a.organization, projectId = _a.projectId, image = _a.image;
        var orgSlug = organization.slug;
        var debugId = image === null || image === void 0 ? void 0 : image.debug_id;
        if (!orgSlug || !projectId || !debugId) {
            return undefined;
        }
        return "/settings/" + orgSlug + "/projects/" + projectId + "/debug-symbols/?query=" + debugId;
    };
    DebugImageDetails.prototype.renderLoading = function () {
        return this.renderBody();
    };
    DebugImageDetails.prototype.renderBody = function () {
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, image = _a.image, organization = _a.organization, projectId = _a.projectId;
        var _b = this.state, loading = _b.loading, builtinSymbolSources = _b.builtinSymbolSources;
        var _c = image !== null && image !== void 0 ? image : {}, debug_id = _c.debug_id, debug_file = _c.debug_file, code_file = _c.code_file, code_id = _c.code_id, architecture = _c.arch, unwind_status = _c.unwind_status, debug_status = _c.debug_status, status = _c.status;
        var candidates = this.getCandidates();
        var baseUrl = this.api.baseUrl;
        var title = getFileName(code_file);
        var imageAddress = image ? <Address image={image}/> : undefined;
        var debugFilesSettingsLink = this.getDebugFilesSettingsLink();
        return (<React.Fragment>
        <Header closeButton>
          <span data-test-id="modal-title">{title !== null && title !== void 0 ? title : t('Unknown')}</span>
        </Header>
        <Body>
          <Content>
            <GeneralInfo>
              <Label>{t('Address Range')}</Label>
              <Value>{imageAddress !== null && imageAddress !== void 0 ? imageAddress : <NotAvailable />}</Value>

              <Label coloredBg>{t('Debug ID')}</Label>
              <Value coloredBg>{debug_id !== null && debug_id !== void 0 ? debug_id : <NotAvailable />}</Value>

              <Label>{t('Debug File')}</Label>
              <Value>{debug_file !== null && debug_file !== void 0 ? debug_file : <NotAvailable />}</Value>

              <Label coloredBg>{t('Code ID')}</Label>
              <Value coloredBg>{code_id !== null && code_id !== void 0 ? code_id : <NotAvailable />}</Value>

              <Label>{t('Code File')}</Label>
              <Value>{code_file !== null && code_file !== void 0 ? code_file : <NotAvailable />}</Value>

              <Label coloredBg>{t('Architecture')}</Label>
              <Value coloredBg>{architecture !== null && architecture !== void 0 ? architecture : <NotAvailable />}</Value>

              <Label>{t('Processing')}</Label>
              <Value>
                {unwind_status || debug_status ? (<Processings unwind_status={unwind_status} debug_status={debug_status}/>) : (<NotAvailable />)}
              </Value>
            </GeneralInfo>
            {debugFilesSettingsLink && (<SearchInSettingsAction>
                <Tooltip title={t('Search for this debug file in all images for the %s project', projectId)}>
                  <Button to={debugFilesSettingsLink} size="small">
                    {t('Search in Settings')}
                  </Button>
                </Tooltip>
              </SearchInSettingsAction>)}
            <Candidates imageStatus={status} candidates={candidates} organization={organization} projectId={projectId} baseUrl={baseUrl} onDelete={this.handleDelete} isLoading={loading} builtinSymbolSources={builtinSymbolSources}/>
          </Content>
        </Body>
        <Footer>
          <Button href="https://docs.sentry.io/platforms/native/data-management/debug-files/" external>
            {t('Read the docs')}
          </Button>
        </Footer>
      </React.Fragment>);
    };
    return DebugImageDetails;
}(AsyncComponent));
export default DebugImageDetails;
var Content = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  font-size: ", ";\n"])), space(3), function (p) { return p.theme.fontSizeMedium; });
var SearchInSettingsAction = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n"])));
var GeneralInfo = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n"])));
var Label = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  ", "\n  padding: ", " ", " ", " ", ";\n"], ["\n  color: ", ";\n  ", "\n  padding: ", " ", " ", " ", ";\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.coloredBg && "background-color: " + p.theme.backgroundSecondary + ";"; }, space(1), space(1.5), space(1), space(1));
var Value = styled(Label)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n  ", "\n  padding: ", ";\n  font-family: ", ";\n  white-space: pre-wrap;\n  word-break: break-all;\n"], ["\n  color: ", ";\n  ", "\n  padding: ", ";\n  font-family: ", ";\n  white-space: pre-wrap;\n  word-break: break-all;\n"])), function (p) { return p.theme.subText; }, function (p) { return p.coloredBg && "background-color: " + p.theme.backgroundSecondary + ";"; }, space(1), function (p) { return p.theme.text.familyMono; });
export var modalCss = css(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  .modal-content {\n    overflow: initial;\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 55%;\n      margin-left: -27.5%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 70%;\n      margin-left: -35%;\n    }\n  }\n"], ["\n  .modal-content {\n    overflow: initial;\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 55%;\n      margin-left: -27.5%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 70%;\n      margin-left: -35%;\n    }\n  }\n"])), theme.breakpoints[0], theme.breakpoints[3]);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=index.jsx.map