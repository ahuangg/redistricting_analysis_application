package com.raven.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.raven.model.State;
import com.raven.repository.StateRepository;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:3000")
public class StateController {
	
	@Autowired
	StateRepository stateRepository;

	@GetMapping("/getState")
	public ResponseEntity<State> getState(@RequestParam String stateName) {
		State state =  stateRepository.findByName(stateName);

		if(state != null){
			return ResponseEntity.ok(state);
		}
		
		return ResponseEntity.notFound().build();		
	}
}
