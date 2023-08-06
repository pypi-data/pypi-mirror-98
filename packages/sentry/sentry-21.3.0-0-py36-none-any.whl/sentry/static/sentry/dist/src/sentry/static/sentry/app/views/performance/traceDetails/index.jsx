import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import withOrganization from 'app/utils/withOrganization';
import TraceDetailsContent from './content';
var TraceSummary = /** @class */ (function (_super) {
    __extends(TraceSummary, _super);
    function TraceSummary() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TraceSummary.prototype.getTraceSlug = function () {
        var traceSlug = this.props.params.traceSlug;
        return typeof traceSlug === 'string' ? traceSlug.trim() : '';
    };
    TraceSummary.prototype.getDocumentTitle = function () {
        return [t('Trace Details'), t('Performance')].join(' - ');
    };
    TraceSummary.prototype.render = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, params = _a.params;
        this.getTraceSlug();
        return (<SentryDocumentTitle title={this.getDocumentTitle()} orgSlug={organization.slug}>
        <StyledPageContent>
          <LightWeightNoProjectMessage organization={organization}>
            <TraceDetailsContent location={location} organization={organization} params={params} traceSlug={this.getTraceSlug()}/>
          </LightWeightNoProjectMessage>
        </StyledPageContent>
      </SentryDocumentTitle>);
    };
    return TraceSummary;
}(React.Component));
export default withOrganization(TraceSummary);
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map