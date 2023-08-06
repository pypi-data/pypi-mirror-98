import React from 'react';
import ExternalLink from 'app/components/links/externalLink';
import { IconMail } from 'app/icons';
import { t } from 'app/locale';
import { UserKnownDataType } from './types';
var EMAIL_REGEX = /[^@]+@[^\.]+\..+/;
function getUserKnownDataDetails(data, type) {
    switch (type) {
        case UserKnownDataType.NAME:
            return {
                subject: t('Name'),
                value: data.name,
            };
        case UserKnownDataType.USERNAME:
            return {
                subject: t('Username'),
                value: data.username,
            };
        case UserKnownDataType.ID:
            return {
                subject: t('ID'),
                value: data.id,
            };
        case UserKnownDataType.IP_ADDRESS:
            return {
                subject: t('IP Address'),
                value: data.ip_address,
            };
        case UserKnownDataType.EMAIL:
            return {
                subject: t('Email'),
                value: data.email,
                subjectIcon: EMAIL_REGEX.test(data.email) && (<ExternalLink href={"mailto:" + data.email} className="external-icon">
            <IconMail size="xs"/>
          </ExternalLink>),
            };
        default:
            return undefined;
    }
}
export default getUserKnownDataDetails;
//# sourceMappingURL=getUserKnownDataDetails.jsx.map