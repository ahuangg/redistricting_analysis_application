import React from "react";
import {
    Card,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeaderCell,
    TableRow,
    Text,
} from "@tremor/react";

import {
    ENSEMBLE_HEADER,
    MEASURE_HEADER,
    HEADER_MAPPING,
} from "@/constants/stringConstants";

import { useAtom } from "jotai";
import {
    clustersAtom,
    currClusterAtom,
    districtPlansAtom,
    currDistrictPlanAtom,
    measureAtom,
    pageStateAtom,
} from "@/atoms/atoms";
import TablePaginator from "./TablePaginator";
import { fetchDistrictPlans } from "@/utils/fetch";

const ClusterAnalysisTable = () => {
    const [clusters, setClusters] = useAtom(clustersAtom);
    const [currCluster, setCurrCluster] = useAtom(currClusterAtom);
    const [districtPlans, setDistrictPlans] = useAtom(districtPlansAtom);
    const [currDistrictPlan, setCurrDistrictPlan] =
        useAtom(currDistrictPlanAtom);
    const [pageState, setPageState] = useAtom(pageStateAtom);
    const [measure, setMeasure] = useAtom(measureAtom);

    const [pageData, setPageData] = React.useState([]);
    const [page, setPage] = React.useState(1);
    const totalPage = Math.ceil(clusters.length / 8);

    React.useEffect(() => {
        setPageData(clusters.slice((page - 1) * 8, page * 8));
    }, [clusters, page]);

    let i: number = 0;

    return (
        <Card className="p-2 h-[434px] shadow-lg">
            <Text className="font-bold p-1">Cluster Analysis Table</Text>

            {clusters.length === 0 ? (
                <Text className="text-center">Select Ensemble to View</Text>
            ) : (
                <React.Fragment>
                    <Table className="h-[355px]">
                        <TableHead>
                            <TableRow>
                                {ENSEMBLE_HEADER.map((item) => {
                                    return (
                                        <TableHeaderCell key={item}>
                                            {HEADER_MAPPING[item]}
                                        </TableHeaderCell>
                                    );
                                })}
                                {MEASURE_HEADER.map((item) => {
                                    return (
                                        <TableHeaderCell key={item}>
                                            {HEADER_MAPPING[item]}
                                        </TableHeaderCell>
                                    );
                                })}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {pageData.map((cluster: any) => {
                                i++;
                                return (
                                    <TableRow
                                        key={cluster.clusterId}
                                        onClick={() => {
                                            if (measure !== "") {
                                                setCurrCluster(cluster);
                                                setCurrDistrictPlan({});
                                                fetchDistrictPlans(
                                                    cluster.districtPlanIds,
                                                    setDistrictPlans
                                                );
                                            }
                                            setPageState("DetailedView");
                                        }}
                                        className={
                                            currCluster?.clusterId ===
                                            cluster?.clusterId
                                                ? "bg-yellow-200"
                                                : i % 2 !== 0
                                                ? "bg-slate-200"
                                                : "bg-white"
                                        }
                                    >
                                        {ENSEMBLE_HEADER.map((item) => {
                                            return (
                                                <TableCell key={item}>
                                                    {cluster[item]}
                                                </TableCell>
                                            );
                                        })}
                                        {MEASURE_HEADER.map((item) => {
                                            return (
                                                <TableCell key={item}>
                                                    {parseFloat(
                                                        cluster.measureData[
                                                            item
                                                        ]
                                                    ).toFixed(2)}
                                                </TableCell>
                                            );
                                        })}
                                    </TableRow>
                                );
                            })}
                        </TableBody>
                    </Table>

                    <TablePaginator
                        page={page}
                        totalPages={totalPage}
                        setPage={setPage}
                    />
                </React.Fragment>
            )}
        </Card>
    );
};

export default ClusterAnalysisTable;
