package com.raven.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import com.raven.model.Boundary;

public interface BoundaryRepository extends MongoRepository<Boundary, String>{ 
	public Boundary findByBoundaryId(int boundaryId);
}
