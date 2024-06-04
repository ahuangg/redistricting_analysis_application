import React from "react";
import { MapContainer, TileLayer, GeoJSON } from "react-leaflet";
import { FullscreenControl } from "react-leaflet-fullscreen";
import { leafletConfig } from "@/constants/config";
import { Card } from "@tremor/react";

import { useAtom } from "jotai";
import { pageStateAtom, currStateAtom, boundaryAtom } from "@/atoms/atoms";

const Map = () => {
    const [pageState, setPageState] = useAtom(pageStateAtom);
    const [currState, setCurrState] = useAtom(currStateAtom);
    const [boundary] = useAtom(boundaryAtom);

    return (
        <Card className="p-2 shadow-lg">
            <MapContainer
                key={currState}
                center={leafletConfig.center[currState]}
                zoom={leafletConfig.zoom[currState]}
                maxZoom={leafletConfig.maxZoom[currState]}
                minZoom={leafletConfig.zoom[currState]}
                maxBounds={leafletConfig.maxBounds[currState]}
                zoomControl={true}
                className={`${
                    pageState === "MapView" ? "h-[880px]" : "h-[418px]"
                } w-full z-0`}
            >
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                {boundary.geojson && (
                    <GeoJSON
                        key={boundary.boundaryId}
                        data={boundary.geojson}
                        style={{ color: "blue" }}
                        onEachFeature={(feature, layer) => {
                            if (feature.properties && feature.properties.name) {
                                if (currState === "All States") {
                                    layer.on({
                                        click: () => {
                                            setPageState("OverView");
                                            setCurrState(
                                                feature.properties.name
                                            );
                                        },
                                    });
                                }
                                layer.bindTooltip(feature.properties.name, {
                                    permanent: false,
                                    direction: "top",
                                });
                                layer.bindPopup(feature.properties.name);
                            }
                        }}
                    />
                )}
                <FullscreenControl position="topleft" />
            </MapContainer>
        </Card>
    );
};

export default Map;
