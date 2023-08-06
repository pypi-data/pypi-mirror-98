#!/usr/bin/env python3

class ResourceReader:
    @staticmethod
    def read(file: str) -> str:
        with open(file, 'r') as f:
            resource_string = f.read()
        return resource_string
