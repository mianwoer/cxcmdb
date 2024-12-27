"""
2021/4/16 11:56
desc
"""


IFLYTE_SSO_VERIFY_SUCCESS_RESULT = """
        <cas:serviceResponse xmlns:cas='http://www.yale.edu/tp/cas'>
    <cas:authenticationSuccess>
        <cas:user>qizhu2</cas:user>
        <cas:attributes>
            <cas:credentialType>UsernamePasswordCredential</cas:credentialType>
            <cas:samlAuthenticationStatementAuthMethod>urn:oasis:names:tc:SAML:1.0:am:password</cas:samlAuthenticationStatementAuthMethod>
            <cas:isFromNewLogin>false</cas:isFromNewLogin>
            <cas:authenticationDate>2021-04-16T10:48:50.979+08:00[PRC]</cas:authenticationDate>
            <cas:authenticationMethod>RestAuthenticationHandler</cas:authenticationMethod>
            <cas:userSource>1</cas:userSource>
            <cas:userAccount>qizhu2</cas:userAccount>
            <cas:successfulAuthenticationHandlers>RestAuthenticationHandler</cas:successfulAuthenticationHandlers>
            <cas:longTermAuthenticationRequestTokenUsed>false</cas:longTermAuthenticationRequestTokenUsed>
            <cas:userName>朱琪</cas:userName>
            <cas:userId>a36e1feb-9eaf-4bbc-934a-27ee71fcba15</cas:userId>
            </cas:attributes>
    </cas:authenticationSuccess>
</cas:serviceResponse>
        """


IFLYTE_SSO_VERIFY_FAIL_RESULT = """
        <cas:serviceResponse xmlns:cas=\'http://www.yale.edu/tp/cas\'>
    <cas:authenticationFailure code="INVALID_TICKET">Ticket &#39;ST-22425-ELpHsQUuRZOYO4bhCPIkEO5Kpg4-ssodev1&#39; not recognized</cas:authenticationFailure>
</cas:serviceResponse>
        """

IFLYTE_SSO_VERIFY_RAISE_RESULT = """
<cas:serviceResponse xmlns:cas=\'http://www.yale.edu/tp/cas\'>
    <cas:authenticationFailure code="INVALID_TICKET">Ticket &#39;ST-22425-ELpHsQUuRZOYO4bhCPIkEO5Kpg4-ssodev1&#39; not recognized</cas:authenticationFailure>
</cas:serviceResponse
"""
