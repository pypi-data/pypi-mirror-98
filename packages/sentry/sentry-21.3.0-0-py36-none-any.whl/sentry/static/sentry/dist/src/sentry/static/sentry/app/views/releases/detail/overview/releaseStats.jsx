import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import { SectionHeading } from 'app/components/charts/styles';
import Count from 'app/components/count';
import DeployBadge from 'app/components/deployBadge';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import NotAvailable from 'app/components/notAvailable';
import QuestionTooltip from 'app/components/questionTooltip';
import TimeSince from 'app/components/timeSince';
import Tooltip from 'app/components/tooltip';
import NOT_AVAILABLE_MESSAGES from 'app/constants/notAvailableMessages';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { getTermHelp, PERFORMANCE_TERM } from 'app/views/performance/data';
import { getSessionTermDescription, SessionTerm, sessionTerm, } from 'app/views/releases/utils/sessionTerm';
import CrashFree from '../../list/crashFree';
import ReleaseAdoption from '../../list/releaseAdoption';
import { DisplayOption } from '../../list/utils';
import { getReleaseNewIssuesUrl, getReleaseUnhandledIssuesUrl } from '../../utils';
import { getReleaseEventView } from '../utils';
function ReleaseStats(_a) {
    var _b;
    var organization = _a.organization, release = _a.release, project = _a.project, location = _a.location, selection = _a.selection;
    var lastDeploy = release.lastDeploy, dateCreated = release.dateCreated, newGroups = release.newGroups, version = release.version;
    var hasHealthData = project.hasHealthData, healthData = project.healthData;
    var sessionsCrashed = healthData.sessionsCrashed, adoption = healthData.adoption, sessionsAdoption = healthData.sessionsAdoption, crashFreeUsers = healthData.crashFreeUsers, crashFreeSessions = healthData.crashFreeSessions, totalUsers24h = healthData.totalUsers24h, totalProjectUsers24h = healthData.totalProjectUsers24h, totalSessions24h = healthData.totalSessions24h, totalProjectSessions24h = healthData.totalProjectSessions24h;
    return (<Container>
      <div>
        <SectionHeading>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? t('Date Deployed') : t('Date Created')}
        </SectionHeading>
        <SectionContent>
          <TimeSince date={(_b = lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) !== null && _b !== void 0 ? _b : dateCreated}/>
        </SectionContent>
      </div>

      <div>
        <SectionHeading>{t('Last Deploy')}</SectionHeading>
        <SectionContent>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? (<DeployBadge deploy={lastDeploy} orgSlug={organization.slug} version={version} projectId={project.id}/>) : (<NotAvailable />)}
        </SectionContent>
      </div>

      <CrashFreeSection>
        <SectionHeading>
          {t('Crash Free Rate')}
          <QuestionTooltip position="top" title={getSessionTermDescription(SessionTerm.CRASH_FREE, project.platform)} size="sm"/>
        </SectionHeading>
        <SectionContent>
          {defined(crashFreeSessions) || defined(crashFreeUsers) ? (<CrashFreeWrapper>
              {defined(crashFreeSessions) && (<div>
                  <CrashFree percent={crashFreeSessions} iconSize="md" displayOption={DisplayOption.SESSIONS}/>
                </div>)}

              {defined(crashFreeUsers) && (<div>
                  <CrashFree percent={crashFreeUsers} iconSize="md" displayOption={DisplayOption.USERS}/>
                </div>)}
            </CrashFreeWrapper>) : (<NotAvailable tooltip={NOT_AVAILABLE_MESSAGES.releaseHealth}/>)}
        </SectionContent>
      </CrashFreeSection>

      <AdoptionSection>
        <SectionHeading>
          {t('Adoption')}
          <QuestionTooltip position="top" title={getSessionTermDescription(SessionTerm.ADOPTION, project.platform)} size="sm"/>
        </SectionHeading>
        <SectionContent>
          {defined(adoption) || defined(sessionsAdoption) ? (<AdoptionWrapper>
              {defined(sessionsAdoption) && (<ReleaseAdoption releaseCount={totalSessions24h !== null && totalSessions24h !== void 0 ? totalSessions24h : 0} projectCount={totalProjectSessions24h !== null && totalProjectSessions24h !== void 0 ? totalProjectSessions24h : 0} adoption={sessionsAdoption} displayOption={DisplayOption.SESSIONS} withLabels/>)}

              {defined(adoption) && (<ReleaseAdoption releaseCount={totalUsers24h !== null && totalUsers24h !== void 0 ? totalUsers24h : 0} projectCount={totalProjectUsers24h !== null && totalProjectUsers24h !== void 0 ? totalProjectUsers24h : 0} adoption={adoption} displayOption={DisplayOption.USERS} withLabels/>)}
            </AdoptionWrapper>) : (<NotAvailable tooltip={NOT_AVAILABLE_MESSAGES.releaseHealth}/>)}
        </SectionContent>
      </AdoptionSection>

      <LinkedStatsSection>
        <div>
          <SectionHeading>{t('New Issues')}</SectionHeading>
          <SectionContent>
            <Tooltip title={t('Open in Issues')}>
              <GlobalSelectionLink to={getReleaseNewIssuesUrl(organization.slug, project.id, version)}>
                <Count value={newGroups}/>
              </GlobalSelectionLink>
            </Tooltip>
          </SectionContent>
        </div>

        <div>
          <SectionHeading>
            {sessionTerm.crashes}
            <QuestionTooltip position="top" title={getSessionTermDescription(SessionTerm.CRASHES, project.platform)} size="sm"/>
          </SectionHeading>
          <SectionContent>
            {hasHealthData ? (<Tooltip title={t('Open in Issues')}>
                <GlobalSelectionLink to={getReleaseUnhandledIssuesUrl(organization.slug, project.id, version)}>
                  <Count value={sessionsCrashed}/>
                </GlobalSelectionLink>
              </Tooltip>) : (<NotAvailable tooltip={NOT_AVAILABLE_MESSAGES.releaseHealth}/>)}
          </SectionContent>
        </div>

        <div>
          <SectionHeading>
            {t('Apdex')}
            <QuestionTooltip position="top" title={getTermHelp(organization, PERFORMANCE_TERM.APDEX)} size="sm"/>
          </SectionHeading>
          <SectionContent>
            <Feature features={['performance-view']}>
              {function (hasFeature) {
        return hasFeature ? (<DiscoverQuery eventView={getReleaseEventView(selection, release === null || release === void 0 ? void 0 : release.version, organization)} location={location} orgSlug={organization.slug}>
                    {function (_a) {
            var isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData;
            if (isLoading ||
                error ||
                !tableData ||
                tableData.data.length === 0) {
                return <NotAvailable />;
            }
            return (<GlobalSelectionLink to={{
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: {
                    query: "release:" + (release === null || release === void 0 ? void 0 : release.version),
                },
            }}>
                          <Tooltip title={t('Open in Performance')}>
                            <Count value={tableData.data[0][getAggregateAlias("apdex(" + organization.apdexThreshold + ")")]}/>
                          </Tooltip>
                        </GlobalSelectionLink>);
        }}
                  </DiscoverQuery>) : (<NotAvailable tooltip={NOT_AVAILABLE_MESSAGES.performance}/>);
    }}
            </Feature>
          </SectionContent>
        </div>
      </LinkedStatsSection>
    </Container>);
}
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 50% 50%;\n  grid-row-gap: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 50% 50%;\n  grid-row-gap: ", ";\n  margin-bottom: ", ";\n"])), space(2), space(3));
var SectionContent = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject([""], [""])));
var CrashFreeSection = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  grid-column: 1/3;\n"], ["\n  grid-column: 1/3;\n"])));
var CrashFreeWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1));
var AdoptionSection = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  grid-column: 1/3;\n  margin-bottom: ", ";\n"], ["\n  grid-column: 1/3;\n  margin-bottom: ", ";\n"])), space(1));
var AdoptionWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1.5));
var LinkedStatsSection = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  grid-column: 1/3;\n  display: flex;\n  justify-content: space-between;\n"], ["\n  grid-column: 1/3;\n  display: flex;\n  justify-content: space-between;\n"])));
export default ReleaseStats;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=releaseStats.jsx.map