package com.raven.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import com.raven.model.State;

public interface StateRepository extends MongoRepository<State, String>{ 
	public State findByName(String name);
}
