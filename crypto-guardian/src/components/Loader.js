import React from 'react';
import { motion } from 'framer-motion';
import { RingLoader } from 'react-spinners';

const Loader = () => {
  return (
    <motion.div
      className="loader"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <RingLoader color="#00aaff" size={60} />
    </motion.div>
  );
};

export default Loader;
