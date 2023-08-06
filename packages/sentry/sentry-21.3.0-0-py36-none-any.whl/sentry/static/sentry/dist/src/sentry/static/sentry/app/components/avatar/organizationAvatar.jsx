import { __extends, __rest } from "tslib";
import React from 'react';
import BaseAvatar from 'app/components/avatar/baseAvatar';
import { explodeSlug } from 'app/utils';
var OrganizationAvatar = /** @class */ (function (_super) {
    __extends(OrganizationAvatar, _super);
    function OrganizationAvatar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationAvatar.prototype.render = function () {
        var _a = this.props, organization = _a.organization, props = __rest(_a, ["organization"]);
        if (!organization) {
            return null;
        }
        var slug = (organization && organization.slug) || '';
        var title = explodeSlug(slug);
        return (<BaseAvatar {...props} type={(organization.avatar && organization.avatar.avatarType) || 'letter_avatar'} uploadPath="organization-avatar" uploadId={organization.avatar && organization.avatar.avatarUuid} letterId={slug} tooltip={slug} title={title}/>);
    };
    return OrganizationAvatar;
}(React.Component));
export default OrganizationAvatar;
//# sourceMappingURL=organizationAvatar.jsx.map