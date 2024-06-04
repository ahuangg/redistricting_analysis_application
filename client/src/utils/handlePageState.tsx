import MapView from "@/components/page-components/MapView";
import OverView from "@/components/page-components/OverView";
import DetailedView from "@/components/page-components/DetailedView";

export const handlePageState = (pageState: string) => {
    switch (pageState) {
        case "MapView":
            return <MapView />;
        case "OverView":
            return <OverView />;
        case "DetailedView":
            return <DetailedView />;
        default:
            return <MapView />;
    }
};
