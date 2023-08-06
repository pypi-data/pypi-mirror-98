import { __assign, __extends } from "tslib";
import React from 'react';
import Breadcrumbs from 'app/components/breadcrumbs';
import { t } from 'app/locale';
import { decodeScalar } from 'app/utils/queryString';
import { transactionSummaryRouteWithQuery } from './transactionSummary/utils';
import { vitalsRouteWithQuery } from './transactionVitals/utils';
import { vitalDetailRouteWithQuery } from './vitalDetail/utils';
import { getPerformanceLandingUrl } from './utils';
var Breadcrumb = /** @class */ (function (_super) {
    __extends(Breadcrumb, _super);
    function Breadcrumb() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Breadcrumb.prototype.getCrumbs = function () {
        var crumbs = [];
        var _a = this.props, organization = _a.organization, location = _a.location, transactionName = _a.transactionName, vitalName = _a.vitalName, eventSlug = _a.eventSlug, traceSlug = _a.traceSlug, transactionComparison = _a.transactionComparison, realUserMonitoring = _a.realUserMonitoring;
        var performanceTarget = {
            pathname: getPerformanceLandingUrl(organization),
            query: __assign(__assign({}, location.query), { 
                // clear out the transaction name
                transaction: undefined }),
        };
        crumbs.push({
            to: performanceTarget,
            label: t('Performance'),
            preserveGlobalSelection: true,
        });
        if (vitalName) {
            var rumTarget = vitalDetailRouteWithQuery({
                orgSlug: organization.slug,
                vitalName: 'fcp',
                projectID: decodeScalar(location.query.project),
                query: location.query,
            });
            crumbs.push({
                to: rumTarget,
                label: t('Vital Detail'),
                preserveGlobalSelection: true,
            });
        }
        else if (transactionName) {
            if (realUserMonitoring) {
                var rumTarget = vitalsRouteWithQuery({
                    orgSlug: organization.slug,
                    transaction: transactionName,
                    projectID: decodeScalar(location.query.project),
                    query: location.query,
                });
                crumbs.push({
                    to: rumTarget,
                    label: t('Web Vitals'),
                    preserveGlobalSelection: true,
                });
            }
            else {
                var summaryTarget = transactionSummaryRouteWithQuery({
                    orgSlug: organization.slug,
                    transaction: transactionName,
                    projectID: decodeScalar(location.query.project),
                    query: location.query,
                });
                crumbs.push({
                    to: summaryTarget,
                    label: t('Transaction Summary'),
                    preserveGlobalSelection: true,
                });
            }
        }
        if (transactionName && eventSlug) {
            crumbs.push({
                to: '',
                label: t('Event Details'),
            });
        }
        else if (transactionComparison) {
            crumbs.push({
                to: '',
                label: t('Compare to Baseline'),
            });
        }
        else if (traceSlug) {
            crumbs.push({
                to: '',
                label: t('Trace View'),
            });
        }
        return crumbs;
    };
    Breadcrumb.prototype.render = function () {
        return <Breadcrumbs crumbs={this.getCrumbs()}/>;
    };
    return Breadcrumb;
}(React.Component));
export default Breadcrumb;
//# sourceMappingURL=breadcrumb.jsx.map