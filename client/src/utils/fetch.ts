import axios from "axios";

const server_url = "http://localhost:8080/api";

export const fetchStateAndBoundary = async (
    stateName: string,
    setState: React.Dispatch<React.SetStateAction<any>>,
    setBoundary: React.Dispatch<React.SetStateAction<any>>,
    setLoading: React.Dispatch<React.SetStateAction<boolean>>
) => {
    try {
        setLoading(true);
        const state = await axios.get(`${server_url}/getState`, {
            params: { stateName: stateName },
        });
        setState(state.data);

        const boundary = await axios.get(`${server_url}/getBoundary`, {
            params: { boundaryId: state.data.boundary },
        });
        setBoundary(boundary.data);

        setLoading(false);
    } catch (err) {
        console.log(err);
    }
};

export const fetchBoundary = async (
    boundaryId: number,

    setDistrictPlanBoundary: React.Dispatch<React.SetStateAction<any>>
) => {
    try {
        const boundary = await axios.get(`${server_url}/getBoundary`, {
            params: { boundaryId: boundaryId },
        });
        setDistrictPlanBoundary(boundary.data);
    } catch (err) {
        console.log(err);
    }
};

export const fetchEnsembles = async (
    state: any,
    setEnsembles: React.Dispatch<React.SetStateAction<any>>
) => {
    try {
        const ensembles = await axios.get(`${server_url}/getEnsembleList`, {
            params: {
                ensembleIds: encodeURIComponent(
                    JSON.stringify(state.ensembleIds)
                ),
            },
        });
        setEnsembles(ensembles.data);
    } catch (err) {
        console.log(err);
    }
};

export const fetchClusters = async (
    currEnsemble: any,
    setClusters: React.Dispatch<React.SetStateAction<any>>
) => {
    try {
        const clusters = await axios.get(`${server_url}/getClusterList`, {
            params: {
                clusterIds: encodeURIComponent(
                    JSON.stringify(currEnsemble.clusterIds)
                ),
            },
        });
        setClusters(clusters.data);
    } catch (err) {
        console.log(err);
    }
};

export const fetchDistrictPlans = async (
    districtPlanIds: any,
    setDistrictPlans: React.Dispatch<React.SetStateAction<any>>
) => {
    try {
        const districtPlans = await axios.get(
            `${server_url}/getDistrictPlanList`,
            {
                params: {
                    districtPlanIds: encodeURIComponent(
                        JSON.stringify(districtPlanIds)
                    ),
                },
            }
        );

        setDistrictPlans(
            districtPlans.data.map((plan: any) => {
                return {
                    ...plan,
                    availability: plan.availability
                        ? "Available"
                        : "Unavailable",
                };
            })
        );
    } catch (err) {
        console.log(err);
    }
};
