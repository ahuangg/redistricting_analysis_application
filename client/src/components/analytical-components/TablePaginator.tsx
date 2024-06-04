import React from "react";
import { Col, Text, Button } from "@tremor/react";

interface TablePaginatorProps {
    page: number;
    totalPages: number;
    setPage: React.Dispatch<React.SetStateAction<number>>;
}
const TablePaginator = (props: TablePaginatorProps) => {
    return (
        <Col className="my-2 flex justify-between items-center">
            <Text>{`Page ${props.page} out of ${props.totalPages}`}</Text>
            <Col>
                <Button
                    size="xs"
                    disabled={props.page <= 1 ? true : false}
                    onClick={() => {
                        props.setPage(props.page - 1);
                    }}
                >
                    Previous
                </Button>
                <Button
                    size="xs"
                    className="ml-2"
                    disabled={props.page >= props.totalPages ? true : false}
                    onClick={() => {
                        props.setPage(props.page + 1);
                    }}
                >
                    Next
                </Button>
            </Col>
        </Col>
    );
};

export default TablePaginator;
