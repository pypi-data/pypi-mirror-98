import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import { INTERNAL_SOURCE } from '../utils';
import Actions from './actions';
import Features from './features';
import Processings from './processings';
import StatusTooltip from './statusTooltip';
import { getSourceTooltipDescription } from './utils';
function Candidate(_a) {
    var candidate = _a.candidate, builtinSymbolSources = _a.builtinSymbolSources, organization = _a.organization, projectId = _a.projectId, baseUrl = _a.baseUrl, onDelete = _a.onDelete;
    var location = candidate.location, download = candidate.download, source_name = candidate.source_name, source = candidate.source;
    var isInternalSource = source === INTERNAL_SOURCE;
    return (<React.Fragment>
      <Column>
        <StatusTooltip candidate={candidate}/>
      </Column>

      <DebugFileColumn>
        <Tooltip title={getSourceTooltipDescription(source, builtinSymbolSources)}>
          <SourceName>{source_name !== null && source_name !== void 0 ? source_name : t('Unknown')}</SourceName>
        </Tooltip>
        {location && !isInternalSource && <Location>{location}</Location>}
      </DebugFileColumn>

      <Column>
        <Processings candidate={candidate}/>
      </Column>

      <Column>
        <Features download={download}/>
      </Column>

      <Column>
        <Actions onDelete={onDelete} baseUrl={baseUrl} projectId={projectId} organization={organization} candidate={candidate} isInternalSource={isInternalSource}/>
      </Column>
    </React.Fragment>);
}
export default Candidate;
var Column = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
// Debug File Info Column
var DebugFileColumn = styled(Column)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-direction: column;\n  align-items: flex-start;\n"], ["\n  flex-direction: column;\n  align-items: flex-start;\n"])));
var SourceName = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  width: 100%;\n  white-space: pre-wrap;\n  word-break: break-all;\n"], ["\n  color: ", ";\n  width: 100%;\n  white-space: pre-wrap;\n  word-break: break-all;\n"])), function (p) { return p.theme.textColor; });
var Location = styled(SourceName)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map