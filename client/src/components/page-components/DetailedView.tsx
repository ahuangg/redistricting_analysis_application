import React from "react";
import { Grid } from "@tremor/react";
import Map from "@/components/analytical-components/Map";
import ClusterAnalysisTable from "@/components/analytical-components/ClusterAnalysisTable";
import DistrictPlansTable from "@/components/analytical-components/DistrictPlansTable";
import ClustersScatterGraph from "@/components/analytical-components/ClustersScatterGraph";

import { useAtom } from "jotai";
import { districtPlansAtom } from "@/atoms/atoms";
import DistrictPlansScatterGraph from "../analytical-components/DistrictPlansScatterGraph";

const DetailedView = () => {
    const [districtPlans, setDistrictPlans] = useAtom(districtPlansAtom);

    return (
        <Grid numItems={2} numItemsLg={2} className="gap-3">
            <Grid className="gap-y-3">
                <Map />
                {districtPlans.length === 0 ? (
                    <ClustersScatterGraph />
                ) : (
                    <DistrictPlansScatterGraph />
                )}
            </Grid>
            <Grid className="gap-y-3">
                <ClusterAnalysisTable />
                <DistrictPlansTable />
            </Grid>
        </Grid>
    );
};

export default DetailedView;
