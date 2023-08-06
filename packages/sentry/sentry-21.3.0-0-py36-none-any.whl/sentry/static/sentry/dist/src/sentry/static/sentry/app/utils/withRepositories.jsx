import { __assign } from "tslib";
import React from 'react';
import createReactClass from 'create-react-class';
import Reflux from 'reflux';
import { getRepositories } from 'app/actionCreators/repositories';
import RepositoryActions from 'app/actions/repositoryActions';
import RepositoryStore from 'app/stores/repositoryStore';
import getDisplayName from 'app/utils/getDisplayName';
var INITIAL_STATE = {
    repositories: undefined,
    repositoriesLoading: undefined,
    repositoriesError: undefined,
};
var withRepositories = function (WrappedComponent) {
    return createReactClass({
        displayName: "withRepositories(" + getDisplayName(WrappedComponent) + ")",
        mixins: [Reflux.listenTo(RepositoryStore, 'onStoreUpdate')],
        getInitialState: function () {
            var organization = this.props.organization;
            var orgSlug = organization.slug;
            var repoData = RepositoryStore.get();
            if (repoData.orgSlug !== orgSlug) {
                RepositoryActions.resetRepositories();
            }
            return repoData.orgSlug === orgSlug
                ? __assign(__assign({}, INITIAL_STATE), repoData) : __assign({}, INITIAL_STATE);
        },
        componentDidMount: function () {
            // XXX(leedongwei): Do not move this function call unless you modify the
            // unit test named "prevents repeated calls"
            this.fetchRepositories();
        },
        fetchRepositories: function () {
            var _a = this.props, api = _a.api, organization = _a.organization;
            var orgSlug = organization.slug;
            var repoData = RepositoryStore.get();
            // XXX(leedongwei): Do not check the orgSlug here. It would have been
            // verified at `getInitialState`. The short-circuit hack in actionCreator
            // does not update the orgSlug in the store.
            if ((!repoData.repositories && !repoData.repositoriesLoading) ||
                repoData.repositoriesError) {
                getRepositories(api, { orgSlug: orgSlug });
            }
        },
        onStoreUpdate: function () {
            var repoData = RepositoryStore.get();
            this.setState(__assign({}, repoData));
        },
        render: function () {
            return <WrappedComponent {...this.props} {...this.state}/>;
        },
    });
};
export default withRepositories;
//# sourceMappingURL=withRepositories.jsx.map