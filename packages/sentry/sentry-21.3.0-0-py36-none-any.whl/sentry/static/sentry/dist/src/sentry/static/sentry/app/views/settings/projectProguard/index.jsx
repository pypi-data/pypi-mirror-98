import { __extends } from "tslib";
import React from 'react';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import withOrganization from 'app/utils/withOrganization';
import ProjectProguard from './projectProguard';
var ProjectProguardContainer = /** @class */ (function (_super) {
    __extends(ProjectProguardContainer, _super);
    function ProjectProguardContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectProguardContainer.prototype.renderNoAccess = function () {
        return (<PageContent>
        <Alert type="warning">{t("You don't have access to this feature")}</Alert>
      </PageContent>);
    };
    ProjectProguardContainer.prototype.render = function () {
        var organization = this.props.organization;
        return (<Feature features={['android-mappings']} organization={organization} renderDisabled={this.renderNoAccess}>
        <ProjectProguard {...this.props}/>
      </Feature>);
    };
    return ProjectProguardContainer;
}(React.Component));
export default withOrganization(ProjectProguardContainer);
//# sourceMappingURL=index.jsx.map