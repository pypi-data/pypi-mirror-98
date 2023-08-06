import { __rest } from "tslib";
import React from 'react';
import Access from 'app/components/acl/access';
import Alert from 'app/components/alert';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
var PermissionAlert = function (_a) {
    var _b = _a.access, access = _b === void 0 ? ['project:write'] : _b, props = __rest(_a, ["access"]);
    return (<Access access={access}>
    {function (_a) {
        var hasAccess = _a.hasAccess;
        return !hasAccess && (<Alert type="warning" icon={<IconWarning size="xs"/>} {...props}>
          {t('These settings can only be edited by users with the organization owner, manager, or admin role.')}
        </Alert>);
    }}
  </Access>);
};
export default PermissionAlert;
//# sourceMappingURL=permissionAlert.jsx.map