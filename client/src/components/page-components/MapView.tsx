import React from "react";
import Map from "../analytical-components/Map";

import { useAtom } from "jotai";
import {
    currStateAtom,
    stateAtom,
    boundaryAtom,
    loadingAtom,
} from "@/atoms/atoms";

import { fetchStateAndBoundary } from "@/utils/fetch";
import Loading from "../general-components/Loading";

const MapView = () => {
    const [loading, setLoading] = useAtom(loadingAtom);
    const [currState, setCurrState] = useAtom(currStateAtom);
    const [boundary, setBoundary] = useAtom(boundaryAtom);
    const [state, setState] = useAtom(stateAtom);

    React.useEffect(() => {
        fetchStateAndBoundary(currState, setState, setBoundary, setLoading);
    }, [currState]);

    if (loading) {
        return <Loading />;
    }

    return <Map />;
};

export default MapView;
