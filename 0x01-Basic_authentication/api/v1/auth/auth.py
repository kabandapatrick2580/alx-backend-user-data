#!/usr/bin/env python3
"""handling auth routes"""
from typing import List, TypeVar
from flask import request

M = TypeVar('M')


class Auth():
    """defining Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth"""
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True
        if path[-1] != '/':
            path += '/'
        for p in excluded_paths:
            if p.endswith('*'):
                if path.startswith(p[:1]):
                    return False
        return False if path in excluded_paths else True

    def authorization_header(self, request=None) -> str:
        """authorization_header"""
        if request:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> M:
        """current_user"""
        return None
