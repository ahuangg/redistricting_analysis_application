package com.raven.controller;

import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.raven.model.Cluster;
import com.raven.repository.ClusterRepository;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:3000")
public class ClusterController {
	
	@Autowired
	ClusterRepository clusterRepository;

	@GetMapping("/getCluster")
	public ResponseEntity<Cluster> getCluster(@RequestParam int clusterId) {
		Cluster cluster =  clusterRepository.findByClusterId(clusterId);

		if(cluster != null){
			return ResponseEntity.ok(cluster);
		}
		
		return ResponseEntity.notFound().build();		
	}

	@GetMapping("/getClusterList")
	public ResponseEntity<List<Cluster>> getEnsembleList(@RequestParam String clusterIds) throws JsonMappingException, JsonProcessingException {
		try {
			String decodedClusterIds = URLDecoder.decode(clusterIds, "UTF-8");
			ObjectMapper objectMapper = new ObjectMapper();
			List<Integer> clusterIdList = objectMapper.readValue(decodedClusterIds, List.class);

			List<Cluster> clusterList = new ArrayList<>();
			
			for(int id : clusterIdList) {
				Cluster cluster =  clusterRepository.findByClusterId(id);
				if (cluster != null) {
					clusterList.add(cluster);
				}
			}

			if(clusterList.size() != 0){
				return ResponseEntity.ok(clusterList);
			}
		}catch(UnsupportedEncodingException e) {
			e.printStackTrace();
		}
		
		return ResponseEntity.notFound().build();		
	}
}
