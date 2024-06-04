import React from "react";
import {
    Card,
    Table,
    Text,
    TableHead,
    TableRow,
    TableBody,
    TableHeaderCell,
    TableCell,
} from "@tremor/react";
import { useAtom } from "jotai";
import { currEnsembleAtom } from "@/atoms/atoms";
import { DISTANCE_HEADER } from "@/constants/stringConstants";

const DistanceMeasureOverview = () => {
    const [currEnsemble, setCurrEnsemble] = useAtom(currEnsembleAtom);

    return (
        <Card className="p-1 shadow-lg h-[434px]">
            <Text className="font-extrabold text-lg pl-1">
                {`Distance Measure Overview`}
            </Text>
            {currEnsemble.distanceMeasureResults === undefined ? (
                <Text className="text-center">Select Ensemble to View</Text>
            ) : (
                <React.Fragment>
                    <Text className=" pl-1">
                        {`Average distance between plans : ${parseFloat(
                            currEnsemble.distanceMeasureResults
                                .averageDistanceBetweenPlans
                        ).toFixed(2)}`}
                    </Text>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableHeaderCell>measure</TableHeaderCell>
                                {DISTANCE_HEADER.map((item) => {
                                    return (
                                        <TableHeaderCell key={item}>
                                            {item}
                                        </TableHeaderCell>
                                    );
                                })}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {["Optimal Transport", "Hamming Distance"].map(
                                (measure) => {
                                    return (
                                        <TableRow key={measure}>
                                            <TableCell>{measure}</TableCell>
                                            {DISTANCE_HEADER.map((item) => {
                                                return (
                                                    <TableCell key={item}>
                                                        {parseFloat(
                                                            currEnsemble
                                                                .distanceMeasureResults
                                                                .results[
                                                                measure
                                                            ][item]
                                                        ).toFixed(2)}
                                                    </TableCell>
                                                );
                                            })}
                                        </TableRow>
                                    );
                                }
                            )}
                        </TableBody>
                    </Table>
                </React.Fragment>
            )}
        </Card>
    );
};

export default DistanceMeasureOverview;
