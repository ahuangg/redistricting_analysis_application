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
import com.raven.model.Ensemble;
import com.raven.repository.EnsembleRepository;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:3000")
public class EnsembleController {
	
	@Autowired
	EnsembleRepository ensembleRepository;

	@GetMapping("/getEnsemble")
	public ResponseEntity<Ensemble> getEnsemble(@RequestParam int ensembleId) {
		Ensemble ensemble =  ensembleRepository.findByEnsembleId(ensembleId);

		if(ensemble != null){
			return ResponseEntity.ok(ensemble);
		}
		
		return ResponseEntity.notFound().build();		
	}

	@GetMapping("/getEnsembleList")
	public ResponseEntity<List<Ensemble>> getEnsembleList(@RequestParam String ensembleIds) throws JsonMappingException, JsonProcessingException {
		try {
			String decodedEnsembleIds = URLDecoder.decode(ensembleIds, "UTF-8");
			ObjectMapper objectMapper = new ObjectMapper();
			List<Integer> ensembleIdList = objectMapper.readValue(decodedEnsembleIds, List.class);

			List<Ensemble> ensembleList = new ArrayList<>();
			
			for(int id : ensembleIdList) {
				Ensemble ensemble =  ensembleRepository.findByEnsembleId(id);
				if (ensemble != null) {
					ensembleList.add(ensemble);
				}
			}

			if(ensembleList.size() != 0){
				return ResponseEntity.ok(ensembleList);
			}
		}catch(UnsupportedEncodingException e) {
			e.printStackTrace();
		}
		
		return ResponseEntity.notFound().build();		
	}
}
