"""
    rabbitmq:
        image: rabbitmq:3.5.7
        ports:
          - 5672:5672
        environment:
            RABBITMQ_DEFAULT_USER: ${RABBITMQ_DEFAULT_USER}
            RABBITMQ_DEFAULT_PASS: ${RABBITMQ_DEFAULT_PASS}
"""
