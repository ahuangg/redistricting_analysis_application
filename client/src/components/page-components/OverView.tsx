import React from "react";
import { Grid } from "@tremor/react";
import Map from "@/components/analytical-components/Map";
import Loading from "@/components/general-components/Loading";
import ClusterAnalysisTable from "@/components/analytical-components/ClusterAnalysisTable";
import LineGraph from "@/components/analytical-components/LineGraph";

import { useAtom } from "jotai";
import {
    currStateAtom,
    stateAtom,
    boundaryAtom,
    loadingAtom,
    ensemblesAtom,
    currEnsembleAtom,
    clustersAtom,
} from "@/atoms/atoms";

import {
    fetchEnsembles,
    fetchStateAndBoundary,
    fetchClusters,
} from "@/utils/fetch";
import DistanceMeasureOverview from "../analytical-components/DistanceMeasureOverview";

const Overview = () => {
    const [loading, setLoading] = useAtom(loadingAtom);
    const [currState, setCurrState] = useAtom(currStateAtom);
    const [boundary, setBoundary] = useAtom(boundaryAtom);
    const [ensembles, setEnsembles] = useAtom(ensemblesAtom);
    const [currEnsemble, setCurrEnsemble] = useAtom(currEnsembleAtom);
    const [clusters, setClusters] = useAtom(clustersAtom);
    const [state, setState] = useAtom(stateAtom);

    React.useEffect(() => {
        fetchStateAndBoundary(currState, setState, setBoundary, setLoading);
    }, [currState]);

    React.useEffect(() => {
        if (Object.keys(state).length > 0 && state.ensembleIds.length > 0) {
            fetchEnsembles(state, setEnsembles);
        }
    }, [state]);

    React.useEffect(() => {
        if (Object.keys(currEnsemble).length > 0) {
            fetchClusters(currEnsemble, setClusters);
        }
    }, [currEnsemble]);

    if (loading) {
        return <Loading />;
    }

    return (
        <Grid numItems={2} numItemsLg={2} className="gap-3">
            <Grid className="gap-y-3">
                <Map />
                <LineGraph />
            </Grid>
            <Grid className="gap-y-3">
                <ClusterAnalysisTable />
                <DistanceMeasureOverview />
            </Grid>
        </Grid>
    );
};

export default Overview;
