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
import com.raven.model.DistrictPlan;
import com.raven.repository.DistrictPlanRepository;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:3000")
public class DistrictPlanController {
	
	@Autowired
	DistrictPlanRepository districtPlanRepository;

	@GetMapping("/getDistrictPlan")
	public ResponseEntity<DistrictPlan> getDistrictPlan(@RequestParam int districtPlanId) {
		DistrictPlan districtPlan =  districtPlanRepository.findByDistrictPlanId(districtPlanId);

		if(districtPlan != null){
			return ResponseEntity.ok(districtPlan);
		}
		
		return ResponseEntity.notFound().build();		
	}

	@GetMapping("/getDistrictPlanList")
	public ResponseEntity<List<DistrictPlan>> getEnsembleList(@RequestParam String districtPlanIds) throws JsonMappingException, JsonProcessingException {
		try {
			String decodedDistrictPlanIds = URLDecoder.decode(districtPlanIds, "UTF-8");
			ObjectMapper objectMapper = new ObjectMapper();
			List<Integer> districtPlanIdsList = objectMapper.readValue(decodedDistrictPlanIds, List.class);

			List<DistrictPlan> districtPlanList = new ArrayList<>();
			
			for(int id : districtPlanIdsList) {
				DistrictPlan cluster =  districtPlanRepository.findByDistrictPlanId(id);
				if (cluster != null) {
					districtPlanList.add(cluster);
				}
			}

			if(districtPlanList.size() != 0){
				return ResponseEntity.ok(districtPlanList);
			}
		}catch(UnsupportedEncodingException e) {
			e.printStackTrace();
		}
		
		return ResponseEntity.notFound().build();		
	}
}
