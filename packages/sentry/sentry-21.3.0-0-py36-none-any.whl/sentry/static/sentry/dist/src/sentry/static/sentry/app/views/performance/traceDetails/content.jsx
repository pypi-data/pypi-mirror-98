import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import * as Layout from 'app/components/layouts/thirds';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
import TraceFullQuery from 'app/utils/performance/quickTrace/traceFullQuery';
import { decodeScalar } from 'app/utils/queryString';
import Breadcrumb from 'app/views/performance/breadcrumb';
import { MetaData } from 'app/views/performance/transactionDetails/styles';
import TraceView from './traceView';
import { getTraceInfo } from './utils';
var TraceDetailsContent = /** @class */ (function (_super) {
    __extends(TraceDetailsContent, _super);
    function TraceDetailsContent() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TraceDetailsContent.prototype.renderTraceLoading = function () {
        return <LoadingIndicator />;
    };
    TraceDetailsContent.prototype.renderTraceRequiresDateRangeSelection = function () {
        return <LoadingError message={t('Trace view requires a date range selection.')}/>;
    };
    TraceDetailsContent.prototype.renderTraceNotFound = function () {
        return <LoadingError message={t('The trace you are looking for was not found.')}/>;
    };
    TraceDetailsContent.prototype.renderTraceHeader = function (traceInfo) {
        return (<TraceDetailHeader>
        <MetaData headingText={t('Transactions')} tooltipText={t('All the transactions that are a part of this trace.')} bodyText={t('%s of %s', traceInfo.relevantTransactions, traceInfo.totalTransactions)} subtext={tn('Across %s project', 'Across %s projects', traceInfo.relevantProjects)}/>
      </TraceDetailHeader>);
    };
    TraceDetailsContent.prototype.renderTraceView = function (trace, traceInfo) {
        return (<TraceDetailBody>
        <TraceView trace={trace} traceInfo={traceInfo}/>
      </TraceDetailBody>);
    };
    TraceDetailsContent.prototype.renderContent = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, traceSlug = _a.traceSlug;
        var query = location.query;
        var start = decodeScalar(query.start);
        var end = decodeScalar(query.end);
        if (!start || !end) {
            Sentry.setTag('current.trace_id', traceSlug);
            Sentry.captureException(new Error('No date range selection found.'));
            return this.renderTraceRequiresDateRangeSelection();
        }
        return (<TraceFullQuery location={location} orgSlug={organization.slug} traceId={traceSlug} start={start} end={end}>
        {function (_a) {
            var isLoading = _a.isLoading, error = _a.error, trace = _a.trace;
            if (isLoading) {
                return _this.renderTraceLoading();
            }
            else if (error !== null || trace === null) {
                return _this.renderTraceNotFound();
            }
            else {
                var traceInfo = getTraceInfo(trace);
                return (<React.Fragment>
                {_this.renderTraceHeader(traceInfo)}
                {_this.renderTraceView(trace, traceInfo)}
              </React.Fragment>);
            }
        }}
      </TraceFullQuery>);
    };
    TraceDetailsContent.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, traceSlug = _a.traceSlug;
        return (<React.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <Breadcrumb organization={organization} location={location} traceSlug={traceSlug}/>
            <Layout.Title data-test-id="trace-header">
              {t('Trace Id: %s', traceSlug)}
            </Layout.Title>
          </Layout.HeaderContent>
        </Layout.Header>
        <Layout.Body>
          <Layout.Main fullWidth>{this.renderContent()}</Layout.Main>
        </Layout.Body>
      </React.Fragment>);
    };
    return TraceDetailsContent;
}(React.Component));
var TraceDetailHeader = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(160px, 1fr) minmax(160px, 1fr) minmax(160px, 1fr) 6fr;\n    grid-row-gap: 0;\n    margin-bottom: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(160px, 1fr) minmax(160px, 1fr) minmax(160px, 1fr) 6fr;\n    grid-row-gap: 0;\n    margin-bottom: 0;\n  }\n"])), space(2), space(2), function (p) { return p.theme.breakpoints[1]; });
var TraceDetailBody = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(3));
export default TraceDetailsContent;
var templateObject_1, templateObject_2;
//# sourceMappingURL=content.jsx.map