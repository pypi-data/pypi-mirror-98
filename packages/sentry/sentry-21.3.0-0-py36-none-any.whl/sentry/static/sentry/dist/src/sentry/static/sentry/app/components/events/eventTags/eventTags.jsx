import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import isEmpty from 'lodash/isEmpty';
import EventDataSection from 'app/components/events/eventDataSection';
import Pills from 'app/components/pills';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { defined, generateQueryWithTag } from 'app/utils';
import EventTagsPill from './eventTagsPill';
var EventTags = function (_a) {
    var tags = _a.event.tags, organization = _a.organization, projectId = _a.projectId, location = _a.location, hasQueryFeature = _a.hasQueryFeature;
    if (isEmpty(tags)) {
        return null;
    }
    var orgSlug = organization.slug;
    var streamPath = "/organizations/" + orgSlug + "/issues/";
    var releasesPath = "/organizations/" + orgSlug + "/releases/";
    return (<StyledEventDataSection title={t('Tags')} type="tags">
      <Pills>
        {tags.map(function (tag, index) { return (<EventTagsPill key={!defined(tag.key) ? "tag-pill-" + index : tag.key} tag={tag} projectId={projectId} organization={organization} location={location} query={generateQueryWithTag(location.query, tag)} streamPath={streamPath} releasesPath={releasesPath} hasQueryFeature={hasQueryFeature}/>); })}
      </Pills>
    </StyledEventDataSection>);
};
export default EventTags;
var StyledEventDataSection = styled(EventDataSection)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-bottom: ", ";\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-bottom: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[1]; }, space(3));
var templateObject_1;
//# sourceMappingURL=eventTags.jsx.map