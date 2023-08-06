import { __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import NotAvailable from 'app/components/notAvailable';
import QuestionTooltip from 'app/components/questionTooltip';
import space from 'app/styles/space';
import { CandidateDownloadStatus, } from 'app/types/debugImage';
import { getFeatureLabel } from './utils';
function Features(_a) {
    var download = _a.download;
    if (download.status !== CandidateDownloadStatus.OK &&
        download.status !== CandidateDownloadStatus.DELETED) {
        return <NotAvailable />;
    }
    var features = Object.entries(download.features).filter(function (_a) {
        var _b = __read(_a, 2), _key = _b[0], value = _b[1];
        return value;
    });
    if (!features.length) {
        return <NotAvailable />;
    }
    return (<Wrapper>
      {features.map(function (_a) {
        var _b = __read(_a, 1), key = _b[0];
        var _c = getFeatureLabel(key), label = _c.label, description = _c.description;
        return (<Feature key={key}>
            {label}
            <QuestionTooltip title={description} size="xs"/>
          </Feature>);
    })}
    </Wrapper>);
}
export default Features;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  font-size: ", ";\n  color: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  font-size: ", ";\n  color: ", ";\n"])), space(1.5), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; });
var Feature = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  align-items: center;\n"])), space(0.5));
var templateObject_1, templateObject_2;
//# sourceMappingURL=features.jsx.map