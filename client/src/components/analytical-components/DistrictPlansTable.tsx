import React, { useState } from "react";
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
    DISTRICT_PLAN_HEADER,
    DISTRICT_PLAN_MEASURE_HEADER,
    HEADER_MAPPING,
} from "@/constants/stringConstants";

import { useAtom } from "jotai";
import { currDistrictPlanAtom, districtPlansAtom } from "@/atoms/atoms";
import TablePaginator from "./TablePaginator";

const DistrictPlansTable = () => {
    const [districtPlans, setDistrictPlans] = useAtom(districtPlansAtom);
    const [currDistrictPlan, setCurrDistrictPlan] =
        useAtom(currDistrictPlanAtom);

    const [pageData, setPageData] = React.useState([]);
    const [page, setPage] = React.useState(1);
    const totalPage = Math.ceil(districtPlans.length / 8);

    React.useEffect(() => {
        setPageData(districtPlans.slice((page - 1) * 8, page * 8));
    }, [districtPlans, page]);

    let i: number = 0;

    return (
        <Card className="p-2 h-[438px] shadow-lg">
            <Text className="font-bold p-1">District Plans Table</Text>

            {districtPlans.length === 0 ? (
                <Text className="text-center">Select a Cluster to View</Text>
            ) : (
                <React.Fragment>
                    <Table className="h-[355px]">
                        <TableHead>
                            <TableRow key={""}>
                                {DISTRICT_PLAN_HEADER.map((item) => {
                                    return (
                                        <TableHeaderCell key={item}>
                                            {HEADER_MAPPING[item]}
                                        </TableHeaderCell>
                                    );
                                })}
                                {DISTRICT_PLAN_MEASURE_HEADER.map((item) => {
                                    return (
                                        <TableHeaderCell key={item}>
                                            {HEADER_MAPPING[item]}
                                        </TableHeaderCell>
                                    );
                                })}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {pageData.map((plan: any) => {
                                i++;
                                return (
                                    <TableRow
                                        key={plan.clusterId}
                                        className={
                                            currDistrictPlan?.districtPlanId ===
                                            plan?.districtPlanId
                                                ? "bg-yellow-200"
                                                : i % 2 !== 0
                                                ? "bg-slate-200"
                                                : "bg-white"
                                        }
                                    >
                                        {DISTRICT_PLAN_HEADER.map((item) => {
                                            return (
                                                <TableCell key={item}>
                                                    {plan[item]}
                                                </TableCell>
                                            );
                                        })}
                                        {DISTRICT_PLAN_MEASURE_HEADER.map(
                                            (item) => {
                                                return (
                                                    <TableCell key={item}>
                                                        {parseFloat(
                                                            plan.measureData[
                                                                item
                                                            ]
                                                        ).toFixed(2)}
                                                    </TableCell>
                                                );
                                            }
                                        )}
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

export default DistrictPlansTable;
