import React from "react";
import { Grid } from "@tremor/react";
import Map from "@/components/analytical-components/Map";
import EnsemblesTable from "@/components/analytical-components/EnsemblesTable";

import { useAtom } from "jotai";
import {
    currStateAtom,
    stateAtom,
    boundaryAtom,
    loadingAtom,
    ensemblesAtom,
} from "@/atoms/atoms";

import { fetchEnsembles, fetchStateAndBoundary } from "@/utils/fetch";

const EnsembleView = () => {
    const [loading, setLoading] = useAtom(loadingAtom);
    const [currState, setCurrState] = useAtom(currStateAtom);
    const [boundary, setBoundary] = useAtom(boundaryAtom);
    const [ensembles, setEnsembles] = useAtom(ensemblesAtom);

    const [state, setState] = useAtom(stateAtom);

    React.useEffect(() => {
        fetchStateAndBoundary(currState, setState, setBoundary, setLoading);
    }, [currState]);

    React.useEffect(() => {
        if (Object.keys(state).length > 0 && state.ensembleIds.length > 0) {
            fetchEnsembles(state, setEnsembles);
        }
    }, [state]);

    return (
        <Grid numItems={2} numItemsLg={2} className="gap-3">
            <Grid className="gap-y-3">
                <Map />
            </Grid>
            <Grid className="gap-y-3">
                <EnsemblesTable />
            </Grid>
        </Grid>
    );
};

export default EnsembleView;
