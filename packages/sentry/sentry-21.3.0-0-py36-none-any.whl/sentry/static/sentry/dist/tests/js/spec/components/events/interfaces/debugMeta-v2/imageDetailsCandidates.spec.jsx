import { __awaiter, __generator } from "tslib";
import React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import { openModal } from 'app/actionCreators/modal';
import DebugImageDetails, { modalCss, } from 'app/components/events/interfaces/debugMeta-v2/debugImageDetails';
import { getFileName } from 'app/components/events/interfaces/debugMeta-v2/utils';
import GlobalModal from 'app/components/globalModal';
describe('Debug Meta - Image Details Candidates', function () {
    var wrapper;
    var projectId = 'foo';
    // @ts-expect-error
    var organization = TestStubs.Organization();
    // @ts-expect-error
    var eventEntryDebugMeta = TestStubs.EventEntryDebugMeta();
    var data = eventEntryDebugMeta.data;
    var images = data.images;
    var debugImage = images[0];
    beforeAll(function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        // @ts-expect-error
                        MockApiClient.addMockResponse({
                            url: "/projects/" + organization.slug + "/" + projectId + "/files/dsyms/?debug_id=" + debugImage.debug_id,
                            method: 'GET',
                            body: [],
                        });
                        // @ts-expect-error
                        MockApiClient.addMockResponse({
                            url: "/builtin-symbol-sources/",
                            method: 'GET',
                            body: [],
                        });
                        wrapper = mountWithTheme(<GlobalModal />);
                        openModal(function (modalProps) { return (<DebugImageDetails {...modalProps} image={debugImage} organization={organization} projectId={projectId}/>); }, {
                            modalCss: modalCss,
                            onClose: jest.fn(),
                        });
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _a.sent();
                        wrapper.update();
                        return [2 /*return*/];
                }
            });
        });
    });
    it('Image Details Modal is open', function () {
        expect(wrapper.find('[data-test-id="modal-title"]').text()).toEqual(getFileName(debugImage.code_file));
    });
    it('Image Candidates correctly sorted', function () {
        var candidates = wrapper.find('Candidate');
        // Check status order.
        // The UI shall sort the candidates by status. However, this sorting is not alphabetical but in the following order:
        // Permissions -> Failed -> Ok -> Deleted (previous Ok) -> Unapplied -> Not Found
        var statusColumns = candidates
            .find('StatusTag')
            .map(function (statusColumn) { return statusColumn.text(); });
        expect(statusColumns).toEqual(['Failed', 'Failed', 'Failed', 'Deleted']);
        var debugFileColumn = candidates.find('DebugFileColumn');
        // Check source names order.
        // The UI shall sort the candidates by source name (alphabetical)
        var sourceNames = debugFileColumn
            .find('SourceName')
            .map(function (sourceName) { return sourceName.text(); });
        expect(sourceNames).toEqual(['America', 'Austria', 'Belgium', 'Sentry']);
        // Check location order.
        // The UI shall sort the candidates by source location (alphabetical)
        var locations = debugFileColumn.find('Location').map(function (location) { return location.text(); });
        // Only 3 results are returned, as the UI only displays the Location component
        // when the location is defined and when it is not internal
        expect(locations).toEqual(['arizona', 'burgenland', 'brussels']);
    });
});
//# sourceMappingURL=imageDetailsCandidates.spec.jsx.map