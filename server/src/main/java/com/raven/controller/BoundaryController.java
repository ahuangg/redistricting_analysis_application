package com.raven.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.raven.model.Boundary;
import com.raven.repository.BoundaryRepository;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://localhost:3000")
public class BoundaryController {
	
	@Autowired
	BoundaryRepository boundaryRepository;

	@GetMapping("/getBoundary")
	public ResponseEntity<Boundary> getBoundary(@RequestParam int boundaryId) {
		Boundary boundary =  boundaryRepository.findByBoundaryId(boundaryId);

		if(boundary != null){
			return ResponseEntity.ok(boundary);
		}
		
		return ResponseEntity.notFound().build();		
	}
}
