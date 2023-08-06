import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import Collapsible from 'app/components/collapsible';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import Link from 'app/components/links/link';
import { tn } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { SectionHeading, Wrapper } from './styles';
function OtherProjects(_a) {
    var projects = _a.projects, location = _a.location;
    return (<Wrapper>
      <SectionHeading>
        {tn('Other Project for This Release', 'Other Projects for This Release', projects.length)}
      </SectionHeading>

      <Collapsible expandButton={function (_a) {
        var onExpand = _a.onExpand, numberOfCollapsedItems = _a.numberOfCollapsedItems;
        return (<Button priority="link" onClick={onExpand}>
            {tn('Show %s collapsed project', 'Show %s collapsed projects', numberOfCollapsedItems)}
          </Button>);
    }}>
        {projects.map(function (project) { return (<Row key={project.id}>
            <StyledLink to={{
        pathname: location.pathname,
        query: __assign(__assign({}, location.query), { project: project.id, yAxis: undefined }),
    }}>
              <ProjectBadge project={project} avatarSize={16}/>
            </StyledLink>
          </Row>); })}
      </Collapsible>
    </Wrapper>);
}
var Row = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  font-size: ", ";\n  color: ", ";\n  ", "\n"], ["\n  margin-bottom: ", ";\n  font-size: ", ";\n  color: ", ";\n  ", "\n"])), space(0.25), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.blue300; }, overflowEllipsis);
var StyledLink = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-block;\n"], ["\n  display: inline-block;\n"])));
export default OtherProjects;
var templateObject_1, templateObject_2;
//# sourceMappingURL=otherProjects.jsx.map