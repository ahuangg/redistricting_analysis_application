package com.raven.server.controller.impl;

import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.raven.server.controller.InputController;

import java.util.ArrayList;
import java.util.List;

import org.bson.Document;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:3000")
public class InputControllerImpl implements InputController {
    String connectionString = "mongodb://localhost:27017";

    /**
     * Retrieves information about a specific state from the "States" collection in the "ravensDB" MongoDB.
     *
     * @param stateName The name of the state for which information is to be retrieved.
     * @return A ResponseEntity containing the JSON representation of the state's information
     *         Returns null in case of any exceptions during the retrieval process.
     * @throws Exception if an error occurs during the MongoDB operation.
     */
    @GetMapping("/getStateInfo")
    @Override
    public ResponseEntity<String> getStateInfo(@RequestParam String stateName) {

        try (MongoClient mongoClient = new MongoClient(new MongoClientURI(connectionString))) {
            MongoDatabase database = mongoClient.getDatabase("ravensDB");
            MongoCollection<Document> statesCollection = database.getCollection("States");
            Document query = new Document("stateName",stateName);
            FindIterable<Document> documents = statesCollection.find(query);
            return ResponseEntity.ok(documents.first().toJson());
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }


    /**
     * Retrieves a summary of information for a specific ensemble identified by the provided ensemble ID.
     *
     * @param ensembleID The unique identifier of the ensemble for which information is to be retrieved.
     * @return A ResponseEntity containing the JSON representation of the ensemble's summary
     *         Returns null in case of any exceptions during the retrieval process.
     * @throws Exception if an error occurs during the MongoDB operation.
     */
    @GetMapping("/getEnsembleSummary")
    @Override
    public ResponseEntity<String> getEnsembleSummary(@RequestParam int ensembleID) {

        try (MongoClient mongoClient = new MongoClient(new MongoClientURI(connectionString))) {
            MongoDatabase database = mongoClient.getDatabase("ravensDB");
            MongoCollection<Document> ensemblesCollection = database.getCollection("Ensembles");
            Document query = new Document("id",ensembleID);
            FindIterable<Document> documents = ensemblesCollection.find(query);
            return ResponseEntity.ok(documents.first().toJson());
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }


    /**
     * Retrieves an overview of information for a specific ensemble identified by the provided ensemble ID.
     *
     * This method constructs a JSON representation of the ensemble's overview,
     * including the ensemble ID, name, and the number of plans associated with it.
     *
     * @param ensembleID The unique identifier of the ensemble for which information is to be retrieved.
     * @return A ResponseEntity containing the JSON representation of the ensemble's overview
     *         Returns null in case of any exceptions during the retrieval process.
     * @throws Exception if an error occurs during the MongoDB operation.
     */
    @GetMapping("/getEnsembleOverview")
    @Override
    public ResponseEntity<String> getEnsembleOverview(int ensembleID) {
        try (MongoClient mongoClient = new MongoClient(new MongoClientURI(connectionString))) {
            MongoDatabase database = mongoClient.getDatabase("ravensDB");
            MongoCollection<Document> ensemblesCollection = database.getCollection("Ensembles");
            Document query = new Document("id",ensembleID);
            FindIterable<Document> documents = ensemblesCollection.find(query);
            Integer numberOfPlans = (Integer) documents.first().get("numberOfPlans");
            String ensembleName = (String) documents.first().get("ensembleName");
            String output = "{"
            + "\"id\":\"" + ensembleID + "\","
            + "\"ensembleName\":\"" + ensembleName + "\","
            + "\"numberOfPlans\":" + numberOfPlans 
            + "}";
            return ResponseEntity.ok(output);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }


    /**
     * Retrieves the cluster size association for a specific ensemble identified by the provided ensemble ID.
     *
     * This method fetches information from the "Ensembles" collection in the "ravensDB" MongoDB, specifically
     * the cluster size association associated with the given ensemble ID. The result is returned as an array of Objects.
     *
     * @param ensembleID The unique identifier of the ensemble for which cluster size association is to be retrieved.
     * @return A ResponseEntity containing an array of Objects representing the ensemble's cluster size association
     *         Returns null in case of any exceptions during the retrieval process.
     * @throws Exception if an error occurs during the MongoDB operation.
     */
    @GetMapping("/getEnsembleClusterSizeAssociation")
    @Override
    public ResponseEntity<Object[]> getEnsembleClusterSizeAssociation(@RequestParam int ensembleID) {

        try (MongoClient mongoClient = new MongoClient(new MongoClientURI(connectionString))) {
            MongoDatabase database = mongoClient.getDatabase("ravensDB");
            MongoCollection<Document> ensemblesCollection = database.getCollection("Ensembles");
            Document query = new Document("id",ensembleID);
            FindIterable<Document> documents = ensemblesCollection.find(query);
            List<Object> ensembleClusterSizeAssociation = (List<Object>) documents.first().get("ensembleClusterSizeAssoication");
            return ResponseEntity.ok(ensembleClusterSizeAssociation.toArray());
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }


    /**
     * Retrieves the distance measure results for a specific ensemble identified by the provided ensemble ID.
     *
     * This method fetches information from the "Ensembles" collection in the "ravensDB" MongoDB, specifically
     * the distance measure results associated with the given ensemble ID. The result is returned as an Object.
     *
     * @param ensembleID The unique identifier of the ensemble for which distance measure results are to be retrieved.
     * @return A ResponseEntity containing an Object representing the ensemble's distance measure results
     *         Returns null in case of any exceptions during the retrieval process.
     * @throws Exception if an error occurs during the MongoDB operation.
     */
    @GetMapping("/getDistanceMeasureResults")
    @Override
    public ResponseEntity<Object> getDistanceMeasureResults(@RequestParam int ensembleID) {

        try (MongoClient mongoClient = new MongoClient(new MongoClientURI(connectionString))) {
            MongoDatabase database = mongoClient.getDatabase("ravensDB");
            MongoCollection<Document> ensemblesCollection = database.getCollection("Ensembles");
            Document query = new Document("id",ensembleID);
            FindIterable<Document> documents = ensemblesCollection.find(query);
            Object distanceMeasureResults = (Object) documents.first().get("distanceMeasureResults");
            return ResponseEntity.ok(distanceMeasureResults);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    
    /**
     * Retrieves a summary of information for a list of clusters identified by the provided list of cluster IDs.
     *
     * @param clusterIDs The list of unique identifiers of the clusters for which information is to be retrieved.
     * @return A ResponseEntity containing a list of JSON representations of the clusters' summaries
     *         for the provided IDs.
     *         Returns null in case of any exceptions during the retrieval process.
     * @throws Exception if an error occurs during the MongoDB operation.
     */
    @Override
    @GetMapping("/getClustersSummary")
    public ResponseEntity<List<String>> getClustersSummary(@RequestParam List<Integer> clusterIDs) {
        List<String> output = new ArrayList<>();
        
        try (MongoClient mongoClient = new MongoClient(new MongoClientURI(connectionString))) {
            MongoDatabase database = mongoClient.getDatabase("ravensDB");
            MongoCollection<Document> clustersCollection = database.getCollection("ClustersNew");

            for(Integer clusterID: clusterIDs) {
                Document query = new Document("id",clusterID);
                FindIterable<Document> documents = clustersCollection.find(query);
                if(documents.first() != null){
                    output.add(documents.first().toJson());
                }
            }
            return ResponseEntity.ok(output);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    
    /**
     * Retrieves a summary of information for a specific cluster identified by the provided cluster ID.
     *
     * @param clusterID The unique identifier of the cluster for which information is to be retrieved.
     * @return A ResponseEntity containing the JSON representation of the cluster's summary
     *         Returns null in case of any exceptions during the retrieval process.
     * @throws Exception if an error occurs during the MongoDB operation.
     */
    @GetMapping("/getClusterSummary")
    @Override
    public ResponseEntity<String> getClusterSummary(@RequestParam int clusterID) {

        try (MongoClient mongoClient = new MongoClient(new MongoClientURI(connectionString))) {
            MongoDatabase database = mongoClient.getDatabase("ravensDB");
            MongoCollection<Document> clustersCollection = database.getCollection("ClustersNew");
            Document query = new Document("id",clusterID);
            FindIterable<Document> documents = clustersCollection.find(query);
            return ResponseEntity.ok(documents.first().toJson());
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }


    /**
     * Retrieves a summary of information for a list of district plans identified by the provided list of district plan IDs.
     *
     * @param districtPlanIDs The list of unique identifiers of the district plans for which information is to be retrieved.
     * @return A ResponseEntity containing a list of JSON representations of the district plans' summaries
     *         for the provided IDs.
     *         Returns null in case of any exceptions during the retrieval process.
     * @throws Exception if an error occurs during the MongoDB operation.
     */
    @GetMapping("/getDistrictPlansSummary")
    @Override
    public ResponseEntity<List<String>> getDistrictPlansSummary(List<Integer> districtPlanIDs) {
        List<String> output = new ArrayList<>();

        try (MongoClient mongoClient = new MongoClient(new MongoClientURI(connectionString))) {
            MongoDatabase database = mongoClient.getDatabase("ravensDB");
            MongoCollection<Document> districtPlansCollection = database.getCollection("DistrictPlansNew");
           
            for(Integer districtPlanID: districtPlanIDs) {
                Document query = new Document("id",districtPlanID);
                FindIterable<Document> documents = districtPlansCollection.find(query);
                if(documents.first() != null){
                    output.add(documents.first().toJson());
                }
            }
            return ResponseEntity.ok(output);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }


    /**
     * Retrieves a summary of information for a specific district plan identified by the provided district plan ID.
     *
     * @param districtPlanID The unique identifier of the district plan for which information is to be retrieved.
     * @return A ResponseEntity containing the JSON representation of the district plan's summary
     *         Returns null in case of any exceptions during the retrieval process.
     * @throws Exception if an error occurs during the MongoDB operation.
     */
    @GetMapping("/getDistrictPlanSummary")
    @Override
    public ResponseEntity<String> getDistrictPlanSummary(@RequestParam int districtPlanID) {

        try (MongoClient mongoClient = new MongoClient(new MongoClientURI(connectionString))) {
            MongoDatabase database = mongoClient.getDatabase("ravensDB");
            MongoCollection<Document> districtPlansCollection = database.getCollection("DistrictPlansNew");
            Document query = new Document("id",districtPlanID);
            FindIterable<Document> documents = districtPlansCollection.find(query);
            return ResponseEntity.ok(documents.first().toJson());
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    
    /**
     * Retrieves the GeoJSON representation of a specific boundary identified by the provided boundary ID.
     *
     * @param boundaryID The unique identifier of the boundary for which GeoJSON is to be retrieved.
     * @return A ResponseEntity containing the GeoJSON representation of the boundary
     *         Returns null in case of any exceptions during the retrieval process.
     * @throws Exception if an error occurs during the MongoDB operation.
     */
    @GetMapping("/getBoundaryGeoJSON")
    @Override
    public ResponseEntity<String> getBoundaryGeoJSON(@RequestParam int boundaryID) {

        try (MongoClient mongoClient = new MongoClient(new MongoClientURI(connectionString))) {
            MongoDatabase database = mongoClient.getDatabase("ravensDB");
            MongoCollection<Document> boundaryGeoJSONsCollection = database.getCollection("BoundaryGeoJSONs");
            Document query = new Document("id",boundaryID);
            FindIterable<Document> documents = boundaryGeoJSONsCollection.find(query);
            return ResponseEntity.ok(documents.first().toJson());
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

}
