import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ExternalLink from 'app/components/links/externalLink';
import Link from 'app/components/links/link';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import getDynamicText from 'app/utils/getDynamicText';
import Field from 'app/views/settings/components/forms/field';
import TextCopyInput from 'app/views/settings/components/forms/textCopyInput';
var DEFAULT_PROPS = {
    showDsn: true,
    showDsnPublic: true,
    showSecurityEndpoint: true,
    showMinidump: true,
    showUnreal: true,
    showPublicKey: false,
    showSecretKey: false,
    showProjectId: false,
};
var ProjectKeyCredentials = /** @class */ (function (_super) {
    __extends(ProjectKeyCredentials, _super);
    function ProjectKeyCredentials() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showDeprecatedDsn: false,
        };
        _this.toggleDeprecatedDsn = function () {
            _this.setState(function (state) { return ({
                showDeprecatedDsn: !state.showDeprecatedDsn,
            }); });
        };
        return _this;
    }
    ProjectKeyCredentials.prototype.render = function () {
        var showDeprecatedDsn = this.state.showDeprecatedDsn;
        var _a = this.props, projectId = _a.projectId, data = _a.data, showDsn = _a.showDsn, showDsnPublic = _a.showDsnPublic, showSecurityEndpoint = _a.showSecurityEndpoint, showMinidump = _a.showMinidump, showUnreal = _a.showUnreal, showPublicKey = _a.showPublicKey, showSecretKey = _a.showSecretKey, showProjectId = _a.showProjectId;
        return (<React.Fragment>
        {showDsnPublic && (<Field label={t('DSN')} inline={false} flexibleControlStateSize help={tct('The DSN tells the SDK where to send the events to. [link]', {
            link: showDsn ? (<Link to="" onClick={this.toggleDeprecatedDsn}>
                  {showDeprecatedDsn
                ? t('Hide deprecated DSN')
                : t('Show deprecated DSN')}
                </Link>) : null,
        })}>
            <TextCopyInput>
              {getDynamicText({
            value: data.dsn.public,
            fixed: '__DSN__',
        })}
            </TextCopyInput>
            {showDeprecatedDsn && (<StyledField label={null} help={t('Deprecated DSN includes a secret which is no longer required by newer SDK versions. If you are unsure which to use, follow installation instructions for your language.')} inline={false} flexibleControlStateSize>
                <TextCopyInput>
                  {getDynamicText({
            value: data.dsn.secret,
            fixed: '__DSN_DEPRECATED__',
        })}
                </TextCopyInput>
              </StyledField>)}
          </Field>)}

        
        {!showDsnPublic && showDsn && (<Field label={t('DSN (Deprecated)')} help={t('Deprecated DSN includes a secret which is no longer required by newer SDK versions. If you are unsure which to use, follow installation instructions for your language.')} inline={false} flexibleControlStateSize>
            <TextCopyInput>
              {getDynamicText({
            value: data.dsn.secret,
            fixed: '__DSN_DEPRECATED__',
        })}
            </TextCopyInput>
          </Field>)}

        {showSecurityEndpoint && (<Field label={t('Security Header Endpoint')} help={t('Use your security header endpoint for features like CSP and Expect-CT reports.')} inline={false} flexibleControlStateSize>
            <TextCopyInput>
              {getDynamicText({
            value: data.dsn.security,
            fixed: '__SECURITY_HEADER_ENDPOINT__',
        })}
            </TextCopyInput>
          </Field>)}

        {showMinidump && (<Field label={t('Minidump Endpoint')} help={tct('Use this endpoint to upload [link], for example with Electron, Crashpad or Breakpad.', {
            link: (<ExternalLink href="https://docs.sentry.io/platforms/native/guides/minidumps/">
                    minidump crash reports
                  </ExternalLink>),
        })} inline={false} flexibleControlStateSize>
            <TextCopyInput>
              {getDynamicText({
            value: data.dsn.minidump,
            fixed: '__MINIDUMP_ENDPOINT__',
        })}
            </TextCopyInput>
          </Field>)}

        {showUnreal && (<Field label={t('Unreal Engine 4 Endpoint')} help={t('Use this endpoint to configure your UE4 Crash Reporter.')} inline={false} flexibleControlStateSize>
            <TextCopyInput>
              {getDynamicText({
            value: data.dsn.unreal || '',
            fixed: '__UNREAL_ENDPOINT__',
        })}
            </TextCopyInput>
          </Field>)}

        {showPublicKey && (<Field label={t('Public Key')} inline flexibleControlStateSize>
            <TextCopyInput>
              {getDynamicText({
            value: data.public,
            fixed: '__PUBLICKEY__',
        })}
            </TextCopyInput>
          </Field>)}

        {showSecretKey && (<Field label={t('Secret Key')} inline flexibleControlStateSize>
            <TextCopyInput>
              {getDynamicText({
            value: data.secret,
            fixed: '__SECRETKEY__',
        })}
            </TextCopyInput>
          </Field>)}

        {showProjectId && (<Field label={t('Project ID')} inline flexibleControlStateSize>
            <TextCopyInput>
              {getDynamicText({
            value: projectId,
            fixed: '__PROJECTID__',
        })}
            </TextCopyInput>
          </Field>)}
      </React.Fragment>);
    };
    ProjectKeyCredentials.defaultProps = DEFAULT_PROPS;
    return ProjectKeyCredentials;
}(React.Component));
var StyledField = styled(Field)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " 0 0 0;\n"], ["\n  padding: ", " 0 0 0;\n"])), space(0.5));
export default ProjectKeyCredentials;
var templateObject_1;
//# sourceMappingURL=projectKeyCredentials.jsx.map